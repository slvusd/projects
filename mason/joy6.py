import time
import board
import busio
from adafruit_pca9685 import PCA9685

# Initialize PCA9685
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # 50Hz like servo tester

ESC_CHANNEL = 15

# Calculate duty cycle values for 50Hz
# Each count = (1000000/50/4096) = 4.88μs
def us_to_duty(microseconds):
    return int((microseconds / 1000000) * pca.frequency * 4096)

MIN_US = 1000
MAX_US = 2000
STEP_US = 40  # Change by 40μs per cycle (every 20ms)

print("Starting auto-sweep mode like servo tester...")
print("NOW plug in your ESC battery!")

current_us = MIN_US
direction = 1  # 1 for increasing, -1 for decreasing

try:
    while True:
        # Set the pulse width
        pca.channels[ESC_CHANNEL].duty_cycle = 1500
        
        # Wait 20ms (50Hz cycle time)
        time.sleep(0.02)
        
except KeyboardInterrupt:
    print("\nStopped")
    pca.deinit()