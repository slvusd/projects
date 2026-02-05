import pygame
import time
import numpy as np
import threading
import queue
import sys
import math
from collections import deque
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton
from PyQt6.QtCore import Qt, QTimer, QPoint
from PyQt6.QtGui import QPainter, QColor, QFont, QPen
from pynput import keyboard

# --- GLOBAL TELEMETRY ---
hud_telemetry = {
    "controls": [0.0, 0.0, 0.0, 0.0, 0.0],
    "thrusters": [0.0] * 6,
    "claw": {"x": 0, "y": 0, "trigger": 0}
}

log_lines = deque(maxlen=6)
log_lock = threading.Lock()

def log(msg: str):
    with log_lock:
        for line in str(msg).splitlines():
            log_lines.append(line)

# --- PYGAME & HARDWARE ---
pygame.init()
pygame.joystick.init()
LEFT_INDEX = None
RIGHT_INDEX = None
calibrated = False 

joystick_count = pygame.joystick.get_count()

if joystick_count >= 2:
    for i in range(joystick_count):
        try: pygame.joystick.Joystick(i).init()
        except: pass

    def do_calibration():
        global LEFT_INDEX, RIGHT_INDEX, calibrated
        while not calibrated:
            for ev in pygame.event.get():
                if ev.type == pygame.JOYBUTTONDOWN:
                    jid = getattr(ev, 'instance_id', getattr(ev, 'joy', None))
                    if jid is None: continue
                    LEFT_INDEX = int(jid)
                    for i in range(joystick_count):
                        if i != LEFT_INDEX:
                            RIGHT_INDEX = i
                            break
                    calibrated = True
            time.sleep(0.05) 
    
    threading.Thread(target=do_calibration, daemon=True).start()

class ROVController:
    def __init__(self):
        self.js_right = self.js_left = None
        r_idx = RIGHT_INDEX if RIGHT_INDEX is not None else 0
        l_idx = LEFT_INDEX if LEFT_INDEX is not None else (1 if r_idx == 0 else 0)
        try:
            if pygame.joystick.get_count() >= 1:
                self.js_right = pygame.joystick.Joystick(r_idx)
            if pygame.joystick.get_count() >= 2:
                self.js_left = pygame.joystick.Joystick(l_idx)
        except: pass
        
        self.mixing_matrix = np.array([
            [1, 1.0, -1, 0.0, 0.0], [1.0, -1.0, 1, 0.0, 0.0],
            [1, -1.0, -1, 0.0, 0.0], [1, -1.0, 1, 0.0, 0.0],
            [0.0, 0.0, 0.0, -1.0, 1.0], [0.0, 0.0, 0.0, -1.0, -1.0]
        ])
        self.deadzone = 0.1
        
    def apply_deadzone(self, value):
        if abs(value) < self.deadzone: return 0.0
        return (value - (self.deadzone if value > 0 else -self.deadzone)) / (1.0 - self.deadzone)
    
    def read_joysticks(self):
        pygame.event.pump()
        controls = np.zeros(5) 
        if self.js_right:
            controls[1] = self.apply_deadzone(self.js_right.get_axis(0)) # Strafe
            controls[0] = self.apply_deadzone(-self.js_right.get_axis(1)) # Forward
            controls[2] = self.apply_deadzone(self.js_right.get_axis(2)) # Yaw
        if self.js_left:
            controls[3] = self.apply_deadzone(-self.js_left.get_axis(1)) # Heave
            controls[4] = self.apply_deadzone(self.js_left.get_axis(0))  # Roll
        return controls

class ClawController:
    def __init__(self, index):
        self.joystick = None
        if index is not None and index < pygame.joystick.get_count():
            self.joystick = pygame.joystick.Joystick(index)

    def read(self):
        if not self.joystick: return 0, 0, 0
        pygame.event.pump()
        x, y = self.joystick.get_hat(0) if self.joystick.get_numhats() > 0 else (0, 0)
        trigger = self.joystick.get_button(0)
        return x, y, trigger

class MovableGhostHUD(QWidget):
    Color_Theme = (255, 50, 200) # Mason's Pink
    
    def __init__(self, stop_event):
        super().__init__()
        self.stop_event = stop_event
        self.is_ghost = True 
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(0, 0, 2560, 1440) 
        
        # Cube Data: 8 vertices of a cube (x, y, z)
        self.points = [
            [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1],
            [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1]
        ]
        # Connections between vertices to draw the edges
        self.edges = [
            (0,1), (1,2), (2,3), (3,0), # Front face
            (4,5), (5,6), (6,7), (7,4), # Back face
            (0,4), (1,5), (2,6), (3,7)  # Connecting lines
        ]

        self.quit_btn = QPushButton("✕", self)
        self.quit_btn.setGeometry(2525, 5, 30, 20)
        self.quit_btn.setStyleSheet("background-color: rgba(255, 0, 0, 100); color: white; border-radius: 5px;")
        self.quit_btn.clicked.connect(self.close_all)

        self.update_window_mode()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100) # 10 FPS for Pi performance

        self.kb_listener = keyboard.Listener(on_press=self.on_press)
        self.kb_listener.start()

    def update_window_mode(self):
        flags = Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool
        if self.is_ghost:
            flags |= Qt.WindowType.WindowTransparentForInput
            self.quit_btn.hide() 
        else:
            self.quit_btn.show()
        self.setWindowFlags(flags)
        self.show()

    def on_press(self, key):
        if key == keyboard.Key.f2:
            self.is_ghost = not self.is_ghost
            QTimer.singleShot(0, self.update_window_mode)

    def draw_3d_rov(self, painter, cx, cy, size, controls):
        """Projects a 3D wireframe cube onto the 2D painter."""
        # Calculate rotation angles based on joystick inputs
        # Fwd/Back = Pitch, Strafe = Roll, Yaw = Yaw
        pitch = controls[0] * 0.5 
        yaw = controls[2] * 0.5
        roll = controls[4] * 0.5
        
        projected_points = []
        for p in self.points:
            x, y, z = p[0], p[1], p[2]
            
            # --- 3D ROTATION MATH ---
            # Rotate X (Pitch)
            ny = y * math.cos(pitch) - z * math.sin(pitch)
            nz = y * math.sin(pitch) + z * math.cos(pitch)
            y, z = ny, nz
            # Rotate Y (Yaw)
            nx = x * math.cos(yaw) + z * math.sin(yaw)
            nz = -x * math.sin(yaw) + z * math.cos(yaw)
            x, z = nx, nz
            # Rotate Z (Roll)
            nx = x * math.cos(roll) - y * math.sin(roll)
            ny = x * math.sin(roll) + y * math.cos(roll)
            x, y = nx, ny

            # Projection: Convert 3D to 2D screen space
            # We multiply by 'size' to scale it up
            px = int(x * size) + cx
            py = int(y * size) + cy
            projected_points.append(QPoint(px, py))

        # Draw the edges
        painter.setPen(QPen(QColor(0, 255, 255, 150), 2))
        for edge in self.edges:
            painter.drawLine(projected_points[edge[0]], projected_points[edge[1]])
        
        # Draw a 'front' indicator (a small cross on the front face)
        painter.setPen(QColor(255, 255, 255, 200))
        painter.drawText(cx - 20, cy - size - 10, "ROV ORIENTATION")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)

        # Main HUD Border
        painter.setPen(QPen(QColor(*self.Color_Theme), 2)) 
        painter.setBrush(QColor(0, 0, 0, 0 if self.is_ghost else 80)) 
        painter.drawRoundedRect(0, 0, self.width()-1, self.height()-1, 15, 15)

        # Telemetry
        painter.setFont(QFont('Consolas', 18))
        painter.setPen(QColor(255, 255, 255, 180))
        c, t, claw = hud_telemetry["controls"], hud_telemetry["thrusters"], hud_telemetry["claw"]
        painter.drawText(20, 80, f"STICK: F:{c[0]:+.2f} S:{c[1]:+.2f} Y:{c[2]:+.2f} H:{c[3]:+.2f}")
        
        # --- DRAW THE 3D MODEL ---
        # Position it in the bottom right area
        self.draw_3d_rov(painter, 2300, 1100, 100, c)

        # Logs
        painter.setFont(QFont('Consolas', 14))
        painter.setPen(QColor(0, 255, 255, 200))
        painter.drawText(20, 260, "--- SYSTEM LOG ---")
        with log_lock:
            for i, line in enumerate(log_lines):
                painter.drawText(20, 285 + (i * 25), f"> {line}")

    def close_all(self):
        self.stop_event.set()
        QApplication.quit()

def rov_logic_thread(stop_event):
    rov = ROVController()
    claw_sys = ClawController(LEFT_INDEX if LEFT_INDEX is not None else 0)
    while not stop_event.is_set():
        controls = rov.read_joysticks()
        thrusters = (rov.mixing_matrix @ controls)
        cx, cy, trigger = claw_sys.read()
        hud_telemetry["controls"], hud_telemetry["thrusters"] = controls, thrusters
        hud_telemetry["claw"] = {"x": cx, "y": cy, "trigger": trigger}
        time.sleep(0.02) 

def main():
    app = QApplication(sys.argv)
    stop_event = threading.Event()
    threading.Thread(target=rov_logic_thread, args=(stop_event,), daemon=True).start()
    hud = MovableGhostHUD(stop_event)
    try: sys.exit(app.exec())
    except KeyboardInterrupt:
        stop_event.set()
        pygame.quit()

if __name__ == "__main__":
    main()
