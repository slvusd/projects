import wiringpi as wp
import time

# GPIO Pin (wiringPi pin numbering scheme)
PWM_PIN = 1  # GPIO 18 is Pin 1 in wiringPi numbering

# Constants
PWM_CLOCK = 192       # Adjust clock for ~50 Hz frequency
PWM_RANGE = 2000      # Full range for PWM in microseconds
NEUTRAL = 1500        # Neutral position (stop motor)
HALF_FORWARD = 1750   # Half-speed forward
HALF_REVERSE = 1250   # Half-speed reverse
FULL_FORWARD = 2000   # Full-speed forward
FULL_REVERSE = 1000   # Full-speed reverse

# Setup
wp.wiringPiSetup()
wp.pinMode(PWM_PIN, wp.PWM_OUTPUT)
wp.pwmSetMode(wp.PWM_MODE_MS)  # Use mark-space mode
wp.pwmSetClock(PWM_CLOCK)      # Set PWM frequency to ~50 Hz
wp.pwmSetRange(PWM_RANGE)      # Set range for pulse widths

def set_pulsewidth(pulsewidth):
    """Convert pulsewidth in microseconds to a PWM value and set it."""
    if pulsewidth < FULL_REVERSE or pulsewidth > FULL_FORWARD:
        print(f"Pulse width {pulsewidth} is out of range!")
        return
    wp.pwmWrite(PWM_PIN, pulsewidth)

try:
    # Initialize ESC (neutral for 2 seconds)
    print("Initializing ESC (neutral position)...")
    set_pulsewidth(NEUTRAL)
    time.sleep(2)

    # Set to half-speed forward
    print("Running motor at half-speed forward...")
    set_pulsewidth(HALF_FORWARD)
    time.sleep(5)

    # Stop motor (neutral position)
    print("Stopping motor...")
    set_pulsewidth(NEUTRAL)
    time.sleep(2)

    # Turn off signal
    print("Turning off signal...")
    wp.pwmWrite(PWM_PIN, 0)

except KeyboardInterrupt:
    print("\nKeyboard interrupt detected. Stopping motor...")
    set_pulsewidth(NEUTRAL)
    time.sleep(2)

finally:
    print("Cleaning up...")
    wp.pwmWrite(PWM_PIN, 0)

