#!/usr/bin/python

# For device documentation, see:
# - https://pcbartists.com/product/i2c-decibel-sound-level-meter-module/
# - https://pcbartists.com/product-documentation/i2c-decibel-meter-programming-manual/
# 

import smbus
import time
from datetime import datetime
from gpiozero import RGBLED, LED
from colorzero import Color

HIGHDB = 90

BUS = smbus.SMBus(1)  # 1 indicates /dev/i2c-1 for pi 5
DECIBEL_I2C_ADDRESS = 0x48
DECIBEL_REGISTER = 0x0a

cled = RGBLED(22, 23, 24)

ROLLING_AVERAGE = 5

secs = [0] * 60

blinking = False


def main():
    while True:
        time.sleep(1)
        vol = get_volume()
        t = datetime.now()
        sec = t.second
        secs[sec % ROLLING_AVERAGE] = vol
        tmax = max(secs[:ROLLING_AVERAGE])
        set_led_color(cled, tmax)
        #print(f'Volume: {vol}: {tmax}')


def get_volume():
    return BUS.read_byte_data(DECIBEL_I2C_ADDRESS, DECIBEL_REGISTER)


def set_led_color(led, volume):
    if volume < HIGHDB-40:
        led.color = (0, 0.2, 0.5)
    if volume < HIGHDB-30:
        led.color = (0, 0.2, 0)
    elif volume < HIGHDB-20:
        led.color = Color('green')
    elif volume < HIGHDB-10:
        led.color = (0.6, 1, 0)
    elif volume < HIGHDB:
        led.color = Color('red')
    else:
        led.blink(on_color=(1,0,0), off_time=0.25, on_time=0.25)


if __name__ == '__main__':
    main()
