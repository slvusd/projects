#In working order as of 1/8/26
from slvrov_tools.legacy_pca9685 import PCA9685_BASIC
import time


FREQ = 50  # Hz
ADDR = 0x40
BUS = 1
pin = 0
driver = PCA9685_BASIC(FREQ, ADDR, BUS)
pins = []

driver.write_duty_cycle(pin, 1000)
time.sleep(3)

while True:
    # 1000 to 2000 in 1 second
    for i in range(1000, 2000, 5):
        driver.write_duty_cycle(pin, i)
        time.sleep(0.001)  # 1 ms delay to create a smooth transition
    print("top")
    time.sleep(0.005)
    # 2000 to 1000 in 1 second
    for i in range(2000, 1000, -5):
        driver.write_duty_cycle(pin, i)
        time.sleep(0.001)  # 1 ms delay to create a smooth transition
    print("bottom")
    time.sleep(0.005)





