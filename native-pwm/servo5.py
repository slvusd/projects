from gpiozero import AngularServo
from time import sleep
import sys

# Define the GPIO pin for the servo
servo_pin = 18  # Change this to your actual GPIO pin

# Create an AngularServo object
servo = AngularServo(servo_pin, min_angle=0, max_angle=180,
                     frequency=50, min_pulse_width=0.001, max_pulse_width=0.002)

def main(angle):
    # Set the servo to the specified angle
    print(f"Setting angle to {angle} degrees")
    servo.angle = angle
    sleep(10)  # Hold the position for 10 seconds
    servo.angle = None  # Stop sending signals to the servo

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 servo_control.py <angle>")
        print("Angle must be between 0 and 180 degrees.")
        sys.exit(1)

    try:
        angle = float(sys.argv[1])
        if angle < 0 or angle > 180:
            raise ValueError("Angle must be between 0 and 180 degrees.")
        
        main(angle)

    except ValueError as e:
        print(e)
        sys.exit(1)

