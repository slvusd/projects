from slvrov_tools.legacy_pca9685 import PCA9685_BASIC

FREQ = 50  # Hz
ADDR = 0x40
BUS = 1

driver = PCA9685_BASIC(FREQ, ADDR, BUS)
pins = []

while True:
    pin, pwm = [int(i) for i in input("> ").strip().split()]
    driver.write_duty_cycle(pin, pwm)
