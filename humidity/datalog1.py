#!/usr/bin/env python
# Eric Brown 27 Nov 2024
# From: https://github.com/adafruit/Adafruit_CircuitPython_AHTx0

import time
import board
import adafruit_ahtx0


# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_ahtx0.AHTx0(i2c)

def c2f(c):
    """
    Convert Celsius to Fahrenheit.
    
    Args:
    celsius (float): Temperature in Celsius
    
    Returns:
    float: Temperature in Fahrenheit
    """
    return (c * 9/5) + 32

while True:
    print(f"Temperature: {sensor.temperature:.1f}°C/{c2f(sensor.temperature):.1f}°F Humidity: {sensor.relative_humidity:.1f}%")
    time.sleep(2)
