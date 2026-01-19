import pygame
from adafruit_pca9685 import PCA9685
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() < 2:
    print(f"Error: Need 2 joysticks, found {pygame.joystick.get_count()}.")
    exit()

# 1. Detect all sticks
all_sticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for s in all_sticks: s.init()

# 2. Calibration: Identify which is which
print("\n--- CALIBRATION ---")
print("Squeeze the TRIGGER (Button 0) on the LEFT joystick...")

left_stick = None
right_stick = None

calibrated = False
while not calibrated:
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            # The first stick to press a button becomes 'left'
            left_instance_id = event.instance_id
            for s in all_sticks:
                if s.get_instance_id() == left_instance_id:
                    left_stick = s
                else:
                    right_stick = s # Assign the other one as right
            print(f"Assigned Stick {left_instance_id} as LEFT.")
            calibrated = True

print("Calibration Complete. Starting monitoring...\n")
led_channel = pca.channels[0]
led.channel.duty_cycle = 0xFFFF
# 3. Main Loop
clock = pygame.time.Clock()
try:
    while True:
        pygame.event.pump()

        # Read Left
        l_x = left_stick.get_axis(0)
        l_y = left_stick.get_axis(1)
        l_z = left_stick.get_axis(2)
        # Read Right
        r_x = right_stick.get_axis(0)
        r_y = right_stick.get_axis(1)
        r_y = right_stick.get_axis(2)
        # Single-line output with labeled sticks
        out = f" [LEFT] X:{l_x:>5.2f} Y:{l_y:>5.2f} Z:{l_z:>5.2f} | [RIGHT] X:{r_x:>5.2f} Y:{r_y:>5.2f} Z:{r_y:>5.2f} "
        print(f"\r{out}\033[K", end="", flush=True)

        clock.tick(60)

except KeyboardInterrupt:
    print("\nExiting...")
finally:
    pygame.quit()
