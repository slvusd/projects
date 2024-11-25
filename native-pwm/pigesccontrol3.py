import pigpio
import signal
from time import sleep

# Constants
ESC_GPIO = 18  # GPIO pin for the ESC
NEUTRAL_PULSE = 1500  # Neutral position (stop) in microseconds
HALF_SPEED_PULSE = 1750  # Half-speed forward in microseconds
FULL_REVERSE_PULSE = 1250  # Example: full reverse in microseconds (varies by ESC)

# Initialize pigpio
pi = pigpio.pi()
if not pi.connected:
    print("Unable to connect to pigpio daemon.")
    exit()

def stop_motor():
    """
    Stops the motor by setting the ESC to the neutral position
    and then detaching the PWM signal.
    """
    print('\nStopping motor...')
    pi.set_servo_pulsewidth(ESC_GPIO, NEUTRAL_PULSE)  # Neutral pulse width
    sleep(0.5)
    pi.set_servo_pulsewidth(ESC_GPIO, 0)  # Stop sending pulses to ESC
    pi.stop()

def handle_exit(sig, frame):
    """
    Handle clean exit when Ctrl+C is pressed.
    """
    stop_motor()
    exit(0)

if __name__ == "__main__":
    try:
        # Set up clean exit on Ctrl+C
        signal.signal(signal.SIGINT, handle_exit)

        # Initialize ESC with neutral signal
        print("Initializing ESC...")
        pi.set_servo_pulsewidth(ESC_GPIO, NEUTRAL_PULSE)
        sleep(2)  # Give ESC time to arm and get ready

        # Set motor to half-speed forward
        print("Running motor at 1/2 speed forward.")
        print("Press Ctrl+C to stop the motor.")
        pi.set_servo_pulsewidth(ESC_GPIO, HALF_SPEED_PULSE)

        # Keep program running until Ctrl+C is pressed
        signal.pause()

    except Exception as e:
        print(f"Something went wrong: {e}")
        stop_motor()

