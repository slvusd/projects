# Eric Brown 26 Nov 2024
# This program worked with the sparkfun PWM (Servo) hat. It is still a
# tad bit finicky as it works between angles of 40 and 140 which is rather
# bizare and due to some poor defaults in ServoKit. Perhaps using the 9685
# library directly will yield better results.

# The sparkfun hat is fine, but a straight 9685 connected via i2c is
# potentially more flexible and is cheaper.

import time
import board
import busio
import sys
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_servokit import ServoKit

# Initialize PCA9685 with 16 channels
kit = ServoKit(channels=16)

# Set the ESC control channel (e.g., channel 0)
esc_channel = 0

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c, gain=1)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)

# Create differential input between channel 0 and 1
#chan = AnalogIn(ads, ADS.P0, ADS.P1)

print("{:>5}\t{:>5}".format('raw', 'v'))

mid=1.608
low_threshold=1.59
high_threshold=1.62
supply_voltage=3.2

while True:
    # voltage goes from 0 to 4.1 with 2.5 being the middle
    if chan.voltage > high_threshold:
        v = (chan.voltage - high_threshold) / (supply_voltage-high_threshold)
        a = 90 + 50 * v
    elif chan.voltage < low_threshold:
        v = chan.voltage / low_threshold
        a = 40 + 50 * v
    else:
        a = 90
    
    kit.servo[0].angle = a
    print("{:>5}\t{:>5.3f}\t{:>5}".format(chan.value, chan.voltage, a))
    time.sleep(0.5)
