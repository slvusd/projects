import time
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio

# Initialize I2C bus
i2c = busio.I2C(SCL, SDA)

# Create the PCA9685 instance
pca = PCA9685(i2c)
pca.frequency = 50  # 50Hz for servos and ESCs

# Function to set the pulse width
def set_pulsewidth(channel, pulsewidth_us):
    """
    Set the PWM pulse width for a specific channel in microseconds.
    """
    pulse_length = 1e6 / pca.frequency  # Pulse length in microseconds
    max_pwm_value = 0xFFFF  # 16-bit PWM resolution
    pwm_value = int((pulsewidth_us / pulse_length) * max_pwm_value)
    pca.channels[channel].duty_cycle = pwm_value

# Constants for ESC pulsewidths
NEUTRAL = 1500  # Neutral position (stop)
HALF_FORWARD = 1750  # Half-speed forward
HALF_REVERSE = 1250  # Half-speed reverse
FULL_FORWARD = 2000  # Full-speed forward
FULL_REVERSE = 1000  # Full-speed reverse

try:
    # Initialize ESC to neutral
    print("Initializing ESC...")
    set_pulsewidth(0, NEUTRAL)  # Servo 0 is channel 0
    time.sleep(2)

    # Run motor at half speed forward
    print("Running motor at half-speed forward...")
    set_pulsewidth(0, HALF_FORWARD)
    time.sleep(5)

    # Stop the motor
    print("Stopping motor...")
    set_pulsewidth(0, NEUTRAL)
    time.sleep(2)

except KeyboardInterrupt:
    print("\nKeyboard interrupt detected. Stopping motor...")
    set_pulsewidth(0, NEUTRAL)

finally:
    print("Cleaning up...")
    pca.deinit()  # Properly release the PCA9685 resources

