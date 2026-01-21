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

THRUSTER_CHANNEL = 0

def us_to_duty(us):
    return int((us / 20000.0) * 4095)

# CRITICAL: Set neutral BEFORE user connects power
pca.channels[THRUSTER_CHANNEL].duty_cycle = us_to_duty(1500)
print("=" * 50)
print("NEUTRAL SIGNAL (1500μs) IS NOW ACTIVE")
print("=" * 50)
print()
print("NOW connect 12V power to the ESC")
print("You should hear:")
print("  - 3 beeps (power)")
print("  - 1 beep (signal detected)")
print("  - 1 beep (ARMED)")
print()
input("Press Enter after you hear 5 beeps...")

print("\nTrying forward motion...")
pca.channels[THRUSTER_CHANNEL].duty_cycle = us_to_duty(1600)
time.sleep(3)

print("Trying more forward...")
pca.channels[THRUSTER_CHANNEL].duty_cycle = us_to_duty(1700)
time.sleep(3)

print("Back to neutral (stop)...")
pca.channels[THRUSTER_CHANNEL].duty_cycle = us_to_duty(1500)
time.sleep(2)

print("Trying reverse...")
pca.channels[THRUSTER_CHANNEL].duty_cycle = us_to_duty(1400)
time.sleep(3)

print("Stop")
pca.channels[THRUSTER_CHANNEL].duty_cycle = us_to_duty(1500)

pca.deinit()
