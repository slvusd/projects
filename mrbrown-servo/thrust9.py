import time
import board
import busio
from adafruit_pca9685 import PCA9685

# Create I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create PCA9685 instance
pca = PCA9685(i2c)

# Set frequency to 50Hz
pca.frequency = 50

THRUSTER_CHANNEL = 14

def us_to_duty(us):
    duty = int((us / 20000.0) * 4095)
    print(f"{us}μs -> duty cycle: {duty}")
    return duty

print("Testing different pulse widths...")
print()

# Try 1500μs
print("Setting 1500μs (should be ~307 duty cycle)")
pca.channels[THRUSTER_CHANNEL].duty_cycle = us_to_duty(1500)
print("Connect ESC power NOW and count beeps")
time.sleep(10)

print("\nTrying 1600μs...")
pca.channels[THRUSTER_CHANNEL].duty_cycle = us_to_duty(1600)
time.sleep(3)

print("Trying 1700μs...")
pca.channels[THRUSTER_CHANNEL].duty_cycle = us_to_duty(1700)
time.sleep(3)

print("Trying 1400μs...")
pca.channels[THRUSTER_CHANNEL].duty_cycle = us_to_duty(1400)
time.sleep(3)

print("Back to 1500μs")
pca.channels[THRUSTER_CHANNEL].duty_cycle = us_to_duty(1500)

pca.deinit()

