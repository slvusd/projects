import board
import busio
import time
from adafruit_pca9685 import PCA9685

i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50

# Constants for 50Hz (16-bit)
STOP = 49151    # 1500us
MAX_FWD = 65535   # 2000us
MAX_REV = 32767   # 1000us

def arm_esc(channel):
    print("Arming ESC... motor must be at neutral.")
    pca.channels[channel].duty_cycle = 5100
    time.sleep(4) # Wait 4 seconds for the ESC to beep/arm
    print("ESC Armed and Ready.")

try:
    arm_esc(0)
    
    # Example: Move slowly forward
    print("Slow Forward...")
    pca.channels[15].duty_cycle = MAX_FWD
    time.sleep(3)
    
    # Back to Stop
    print("Stopping...")
    pca.channels[15].duty_cycle = STOP

except KeyboardInterrupt:
    pca.channels[15].duty_cycle = STOP
    pca.deinit()
