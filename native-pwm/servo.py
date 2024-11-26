from gpiozero import Servo
from time import sleep

# Define the GPIO pin for the servo
servo_pin = 26
servo = Servo(servo_pin, min_pulse_width=0.001, max_pulse_width=0.002)  # Set pulse widths for 1ms to 2ms

def set_angle(angle):
    # Ensure angle is within valid range (40 to 140)
    if angle < 40:
        angle = 40
    elif angle > 140:
        angle = 140
    
    # Map angle (40-140) to a range suitable for Servo (-1 to +1)
    # - Angle 40 corresponds to -1
    # - Angle 90 corresponds to 0
    # - Angle 140 corresponds to +1
    # The mapping is done based on the assumption that your servo can handle angles in this range.
    
    # Convert angle directly to a value for the Servo class:
    normalized_value = (angle - 90) / 50  # This maps 90 to 0, and ranges from -1 to +1
    servo.value = normalized_value

try:
    print("Setting angle to minimum...")
    set_angle(40)  # Minimum angle
    sleep(2)

    print("Setting angle to mid position...")
    set_angle(90)  # Mid position
    sleep(2)

    print("Setting angle to maximum...")
    set_angle(140) # Maximum angle
    sleep(2)

finally:
    servo.value = None  # Stop sending signals (optional cleanup)

