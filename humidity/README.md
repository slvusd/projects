# AHT10 i2c Temperature and Humidity Sensor

We have thermocouples that require voltage division and ADCs to
covert analog to digital. But those don't measure humidity and
are harder to use than a purely digital sensor on i2c.

* Library: adafruit-circuitpython-ahtx0 - see [adafruit github](https://github.com/adafruit/Adafruit_CircuitPython_AHTx0)
* i2c Address: 0x38

## Running Example

Activate the environment and run `ex1.py` and press control-C when done.

    source venv/bin/activate
    python ex1.py

## Notes

### Eric Brown 27 Nov 2024

The example code worked right out of the box. I converted
to fahrenheit and updated the formatted output. Otherwise,
it worked great.

