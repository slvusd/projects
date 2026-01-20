from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16)
kit.frequency = 50  # 50 Hz
esc_channel = 15

# Set pulse width range for the ESC
kit.servo[esc_channel].set_pulse_width_range(1000, 2000)

def esc_write(channel, pulse_us):
    """
    Set the ESC PWM in microseconds.
    - channel: PCA9685 channel (0-15)
    - pulse_us: pulse width in microseconds (1000-2000)
    """
    # Convert microseconds to "angle" 0-180
    min_us = 1000
    max_us = 2000
    pulse_us = max(min_us, min(max_us, pulse_us))  # clamp to min/max
    angle = (pulse_us - min_us) / (max_us - min_us) * 180
    kit.servo[channel].angle = angle

# --- Example usage ---

# Initialize ESC at neutral (1500 µs)
esc_write(esc_channel, 1500)
print("Initializing ESC at 1500 µs")
time.sleep(2)

# Full forward
esc_write(esc_channel, 2000)
print("Full forward (2000 µs)")
time.sleep(2)

# Full reverse
esc_write(esc_channel, 1000)
print("Full reverse (1000 µs)")
time.sleep(2)

# Back to neutral
esc_write(esc_channel, 1500)
print("Neutral")
