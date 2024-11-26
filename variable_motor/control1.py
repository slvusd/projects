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
chan = AnalogIn(ads, ADS.P3)

# Create differential input between channel 0 and 1
#chan = AnalogIn(ads, ADS.P0, ADS.P1)

print("{:>5}\t{:>5}".format('raw', 'v'))

mid=1.608
low_threshold=1.59
high_threshold=1.62

while True:
    # voltage goes from 0 to 4.1 with 2.5 being the middle
    if chan.voltage > high_threshold:
        v = (chan.voltage - high_threshold) / (3.3-high_threshold)
        a = 90 + 50 * v
    elif chan.voltage < low_threshold:
        v = chan.voltage / low_threshold
        a = 40 + 50 * v
    else:
        a = 90
    
    kit.servo[0].angle = a
    print("{:>5}\t{:>5.3f}\t{:>5}".format(chan.value, chan.voltage, a))
    time.sleep(0.5)
