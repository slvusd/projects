import pygame
import time
import numpy as np
import threading
import queue
import sys
from collections import deque

# thread-safe in-memory log for terminal status block
log_lines = deque(maxlen=6)
log_lock = threading.Lock()

def log(msg: str):
    """Append a message to the in-memory log (thread-safe)."""
    with log_lock:
        for line in str(msg).splitlines():
            log_lines.append(line)

pygame.init()
pygame.joystick.init()
LEFT_INDEX = None
RIGHT_INDEX = None

# Calibration: ask the user to press the trigger on the LEFT joystick to identify left/right
joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
    log("No joysticks detected!")
elif joystick_count == 1:
    log("Only 1 joystick detected, requiring 2 for full control.")
elif joystick_count >= 2:
    log(f"{joystick_count} joysticks detected — initialize and calibrate.")
    # initialize all sticks
    sticks = [pygame.joystick.Joystick(i) for i in range(joystick_count)]
    for s in sticks:
        try:
            s.init()
        except Exception:
            pass

    log("--- CALIBRATION ---")
    log("Squeeze the TRIGGER (Button 0) on the LEFT joystick...")
    # Also print an immediate, user-visible prompt to stdout
    print("Please press the LEFT trigger (button 0) on the joystick you want to be LEFT now...")

    calibrated = False
    while not calibrated:
        for ev in pygame.event.get():
            if ev.type == pygame.JOYBUTTONDOWN:
                jid = getattr(ev, 'instance_id', None)
                if jid is None:
                    jid = getattr(ev, 'joy', None)
                if jid is None:
                    continue
                # map jid to joystick index (pygame commonly uses 0..N-1)
                left_idx = int(jid)
                # pick the other stick as right
                right_idx = 0 if left_idx != 0 else (1 if joystick_count > 1 else None)
                for i in range(joystick_count):
                    if i != left_idx:
                        right_idx = i
                        break

                LEFT_INDEX = left_idx
                RIGHT_INDEX = right_idx
                log(f"Assigned stick {LEFT_INDEX} as LEFT and {RIGHT_INDEX} as RIGHT.")
                calibrated = True
        time.sleep(0.01)

    log("Calibration complete.")
    class ROVController:
        def __init__(self):
            # Initialize joysticks
            self.joystick_count = pygame.joystick.get_count()
            if self.joystick_count < 2:
                log(f"Warning: Only {self.joystick_count} joystick(s) detected. Need 2.")
            
            self.js_right = None  # Movement joystick
            self.js_left = None   # Heave joystick
            
            # Determine which physical joystick indices to use (from calibration)
            r_idx = RIGHT_INDEX if RIGHT_INDEX is not None else 0
            l_idx = LEFT_INDEX if LEFT_INDEX is not None else (1 if r_idx == 0 else 0)

            if self.joystick_count >= 1:
                try:
                    self.js_right = pygame.joystick.Joystick(r_idx)
                    self.js_right.init()
                    log(f"Right Stick: {self.js_right.get_name()}")
                except Exception:
                    self.js_right = None

            if self.joystick_count >= 2:
                try:
                    self.js_left = pygame.joystick.Joystick(l_idx)
                    self.js_left.init()
                    log(f"Left Stick: {self.js_left.get_name()}")
                except Exception:
                    self.js_left = None
            
            # Thruster mixing matrix (6 thrusters x 5 DOF)
            # DOF: [Forward, Strafe, Yaw, Heave, Roll]
            # Positions 1-4: Horizontal thrusters for strafing/yaw
            # Positions 5-6: Vertical thrusters for heave
            
            self.mixing_matrix = np.array([
                # Thruster 1 (Front Left, 45° orientation)
                [1, 1.0, -1, 0.0, 0.0],
                
                # Thruster 2 (Front Right, 45° orientation)
                [1.0,  -1.0,  1, 0.0, 0.0],
                
                # Thruster 3 (Rear Left, 45° orientation)
                [1, -1.0,  -1, 0.0, 0.0],
                
                # Thruster 4 (Rear Right, 45° orientation)
                [1,  -1.0, 1, 0.0, 0.0],
                
                # Thruster 5 (Vertical - Top or Bottom)
                [0.0,  0.0,  0.0,  -1.0, 1.0],
                
                # Thruster 6 (Vertical - Top or Bottom)
                [0.0,  0.0,  0.0,  -1.0, -1.0]
            ])
            
            # Deadzone for joystick inputs
            self.deadzone = 0.1
            
            # Maximum thruster output (-1.0 to 1.0)
            self.max_thrust = 1.0
            
        def apply_deadzone(self, value, deadzone=None):
            """Apply deadzone to joystick input"""
            if deadzone is None:
                deadzone = self.deadzone
            
            if abs(value) < deadzone:
                return 0.0
            else:
                # Scale the remaining range to -1.0 to 1.0
                sign = 1 if value > 0 else -1
                return sign * (abs(value) - deadzone) / (1.0 - deadzone)
        
        def read_joysticks(self):
            """Read joystick inputs and return desired movements"""
            pygame.event.pump()
            
            # Initialize control inputs [Forward, Strafe, Yaw, Heave, Roll]
            controls = np.array([0.0, 0.0, 0.0, 0.0, 0.0])  # Added extra for roll 
            if self.js_right:
                # Right stick - X axis (strafe)
                strafe = self.js_right.get_axis(0)  # Left/Right
                controls[1] = self.apply_deadzone(strafe)
                
                # Right stick - Y axis (forward/back)
                forward = -self.js_right.get_axis(1)  # Forward/Back (inverted)
                controls[0] = self.apply_deadzone(forward)
                
                # Right stick - Twist axis (yaw)
                yaw = self.js_right.get_axis(2)  # Rotation
                controls[2] = self.apply_deadzone(yaw)
            
            if self.js_left:
                # Left stick - Y axis (heave/up-down)
                heave = -self.js_left.get_axis(1)  # Up/Down (inverted)
                controls[3] = self.apply_deadzone(heave)

                # Left stick - X axis (roll)
                roll = self.js_left.get_axis(0)  # Roll left/right
                controls[4] = self.apply_deadzone(roll)
            return controls
        
        def calculate_thruster_outputs(self, controls):
            """
            Calculate thruster outputs from control inputs using mixing matrix
            
            Args:
                controls: numpy array [forward, strafe, yaw, heave]
            
            Returns:
                numpy array of 6 thruster values (-1.0 to 1.0)
            """
            # Matrix multiplication: thruster_outputs = mixing_matrix @ controls
            thruster_outputs = self.mixing_matrix @ controls
            
            # Normalize if any thruster exceeds maximum
            max_output = np.max(np.abs(thruster_outputs))
            if max_output > self.max_thrust:
                thruster_outputs = thruster_outputs * (self.max_thrust / max_output)
            
            return thruster_outputs
        
        def map_to_pwm(self, thruster_value, min_pwm=1000, mid_pwm=1500, max_pwm=2000):
            """
            Map thruster value (-1.0 to 1.0) to PWM signal (typically 1100-1900 µs)
            
            Args:
                thruster_value: -1.0 (full reverse) to 1.0 (full forward)
                min_pwm: PWM value for full reverse
                mid_pwm: PWM value for stopped
                max_pwm: PWM value for full forward
            
            Returns:
                PWM value in microseconds
            """
            if thruster_value >= 0:
                # Forward direction
                pwm = mid_pwm + (max_pwm - mid_pwm) * thruster_value
            else:
                # Reverse direction
                pwm = mid_pwm + (mid_pwm - min_pwm) * thruster_value
            
            return int(pwm)
        
        def run(self):
            """Main control loop"""
            log("ROV Thruster Control Active")
            log("Right Stick: Forward/Strafe/Yaw")
            log("Left Stick: Heave (Up/Down)")
            log("Press Ctrl+C to exit")
            
            try:
                while True:
                    # Read joystick inputs
                    controls = self.read_joysticks()
                    
                    # Calculate thruster outputs
                    thrusters = self.calculate_thruster_outputs(controls)
                    
                    # Convert to PWM (example)
                    pwm_values = [self.map_to_pwm(t) for t in thrusters]
                    
                    # Log a snapshot (not for high-frequency logging)
                    log(f"Snapshot: F:{controls[0]:+.2f} S:{controls[1]:+.2f} Y:{controls[2]:+.2f} H:{controls[3]:+.2f}")
                    
                    # Here you would send PWM values to your motor controllers
                    # Example: send_to_thrusters(pwm_values)
                    
                    time.sleep(0.02)  # 50 Hz update rate
                    
            except KeyboardInterrupt:
                log("Shutting down...")
                pygame.quit()
    class ClawController:
        def __init__(self, joystick_index, pca_address=0x40, channel=0):
            joystick_count = pygame.joystick.get_count()
            if joystick_index >= joystick_count:
                raise ValueError(f"Joystick index {joystick_index} not found. Only {joystick_count} joystick(s) detected.")
            
            js = pygame.joystick.Joystick(joystick_index)
            self.joystick = js
            log(f"Joystick {joystick_index} initialized: {js.get_name()}")
        
        def read_joystick(self):
            pygame.event.pump()
            trigger = self.joystick.get_button(0)
            x, y = self.joystick.get_hat(0)
            return x, y, trigger
        
        def run(self):
            try:
                while True:
                    x, y, trigger = self.read_joystick()
                    log(f"Hat position: x={x:2d}, y={y:2d}, Trigger: {trigger}")
                    time.sleep(0.02)  # 50 Hz
            except KeyboardInterrupt:
                log("Exiting...")



def main():
    rov_controller = ROVController()  # ROV controller uses both joysticks internally
    claw_controller = ClawController(0)  # Assuming claw is controlled by first joystick
    # Set up a queue and worker thread to handle hardware I/O (no pygame calls in worker)
    pwm_queue = queue.Queue(maxsize=8)
    stop_event = threading.Event()

    def pwm_worker(q: queue.Queue, stop_evt: threading.Event):
        """Consume PWM lists from queue and send to hardware. Runs in background."""
        while not stop_evt.is_set():
            try:
                pwm = q.get(timeout=0.1)
            except queue.Empty:
                continue
            # Replace this with actual hardware send (e.g., over serial, I2C, etc.)
            # Keep this function free of pygame calls.
            log(f"[pwm_worker] sending: {pwm}")
            q.task_done()

    worker = threading.Thread(target=pwm_worker, args=(pwm_queue, stop_event), daemon=True)
    worker.start()

    try:
        log("Running main event loop on main thread. Press Ctrl+C to exit.")
        # status renderer: prints a fixed multi-line block and updates it in place
        def draw_status(controls, x, y, trigger, thrusters, first=False):
            base_lines = [
                f"Controls: F:{controls[0]:+.2f}  S:{controls[1]:+.2f}  Y:{controls[2]:+.2f}  H:{controls[3]:+.2f}",
                f"Hat: x={x:2d}  y={y:2d}  Trigger:{trigger}",
                "Thrusters: " + " ".join(f"{i+1}:{t:+.2f}" for i, t in enumerate(thrusters)),
                f"Queue size: {pwm_queue.qsize()}"
            ]

            # include recent log lines below the status block
            with log_lock:
                logs = list(log_lines)

            lines = base_lines + (logs if logs else ["(no recent logs)"])

            if not first:
                # move cursor up by number of lines to overwrite the block
                sys.stdout.write(f"\x1b[{len(lines)}A")

            for ln in lines:
                # clear the current line and write
                sys.stdout.write("\x1b[2K")
                sys.stdout.write(ln + "\n")
            sys.stdout.flush()

        first_draw = True

        while True:
            # Poll joysticks / pump events on the main thread (required on macOS)
            controls = rov_controller.read_joysticks()
            thrusters = rov_controller.calculate_thruster_outputs(controls)
            pwm_values = [rov_controller.map_to_pwm(t) for t in thrusters]

            x, y, trigger = claw_controller.read_joystick()

            # Update multi-line status block in-place
            draw_status(controls, x, y, trigger, thrusters, first=first_draw)
            first_draw = False

            # Enqueue PWM values for background worker (non-blocking)
            try:
                pwm_queue.put_nowait(pwm_values)
            except queue.Full:
                # If queue is full, drop this update (keep main loop responsive)
                pass

            time.sleep(0.02)  # 50 Hz update
    except KeyboardInterrupt:
        log("Shutting down...")
        stop_event.set()
        worker.join(timeout=1.0)
        pygame.quit()


if __name__ == "__main__":
    main()
