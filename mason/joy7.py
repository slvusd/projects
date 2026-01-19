from slvrov_tools.legacy_pca9685 import PCA9685_BASIC
import time

FREQ = 50  # Hz
ADDR = 0x40
BUS = 1
ESC_PIN = 15  # Change this to your ESC channel
driver = PCA9685_BASIC(FREQ, ADDR, BUS)
driver.write_duty_cycle(ESC_PIN, 1500)
time.sleep(100000)
