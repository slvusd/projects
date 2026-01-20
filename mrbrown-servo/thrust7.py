import time
import board
import busio
from adafruit_pca9685 import PCA9685

# Create I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create PCA9685 instance
pca = PCA9685(i2c)

# Set frequency to 50Hz (required for ESCs)
pca.frequency = 50

# T200 on channel 0
THRUSTER_CHANNEL = 1

# Convert microseconds to duty cycle value
# PCA9685 is 12-bit (0-4095)
# At 50Hz, each cycle is 20ms (20000μs)
# duty_cycle = (pulse_width_us / 20000) * 4095
def us_to_duty(us):
    return int((us / 20000.0) * 4095)

print("Disconnect ESC power")
time.sleep(2)

# Send 1500μs (neutral)
pca.channels[THRUSTER_CHANNEL].duty_cycle = us_to_duty(1500)
print("Sending 1500μs - now connect ESC power")
print("Listen for 5 beeps")

time.sleep(10)

# Try forward (1600μs)
pca.channels[THRUSTER_CHANNEL].duty_cycle = us_to_duty(1600)
print("Forward")
time.sleep(3)

# Stop (1500μs)
pca.channels[THRUSTER_CHANNEL].duty_cycle = us_to_duty(1500)
print("Stopped")

pca.deinit()

