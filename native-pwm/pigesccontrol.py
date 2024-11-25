import pigpio
import time

# GPIO pin where the ESC is connected
ESC_GPIO = 18

# Pulse width values in microseconds
MIN_PULSE = 1000  # Minimum throttle
MAX_PULSE = 2000  # Maximum throttle
HALF_SPEED_PULSE = (MIN_PULSE + MAX_PULSE) // 2  # 1500 µs for half speed
FREQUENCY = 50

# Initialize pigpio
pi = pigpio.pi()

if not pi.connected:
    print("Unable to connect to pigpio daemon.")
    exit()

try:
    # Set GPIO mode to output
    pi.set_mode(ESC_GPIO, pigpio.OUTPUT)
    pi.set_PWM_frequency(ESC_GPIO, FREQUENCY)

    # Initialize ESC with a neutral signal (e.g., 1500 µs for many ESCs)
    print("Initializing ESC. Please wait...")
    pi.set_servo_pulsewidth(ESC_GPIO, 1500)  # Neutral signal
    time.sleep(2)  # Give the ESC time to initialize

    # Set to half speed
    print("Setting motor to half speed.")
    pi.set_servo_pulsewidth(ESC_GPIO, MAX_PULSE)
    time.sleep(5)  # Run at half speed for 5 seconds

    # Stop the motor
    print("Stopping motor.")
    pi.set_servo_pulsewidth(ESC_GPIO, 0)  # Stop signal

finally:
    # Clean up
    pi.set_servo_pulsewidth(ESC_GPIO, 0)  # Ensure motor is stopped
    pi.stop()

