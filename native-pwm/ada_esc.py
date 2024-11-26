from time import sleep
from adafruit_servokit import ServoKit

# Initialize PCA9685 with 16 channels
kit = ServoKit(channels=16)

# Set the ESC control channel (e.g., channel 0)
esc_channel = 0

# Function to set ESC throttle using pulse width in milliseconds
def set_throttle(pulse_width_ms):
    # Map pulse width to angle (0-180) for the ServoKit library
    # 1ms = 0 degrees, 2ms = 180 degrees
    angle = (pulse_width_ms - 1) * 180 / 1
    kit.servo[esc_channel].angle = angle
    print(f"pw: {pulse_width_ms} =angle:{angle}")

kit.servo[0].angle=40
sleep(1)
# Example usage
set_throttle(1.5)  # Stop (neutral position)
sleep(1)
set_throttle(1)    # Full reverse
sleep(3)
set_throttle(2)    # Full forward
sleep(3)
set_throttle(1.5)

