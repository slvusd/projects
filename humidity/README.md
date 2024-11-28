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

Ran the following to get things working:

    python -m venv venv
    source venv/bin/activate
    pip install adafruit-circuitpython-ahtx0
    pip freeze > requirements.txt
    python ex1.py

Explanation:

* `python -m venv venv` creates a virtual environment
  so `pip` can be run without impacting system environment
  or needing to be root.
* `source venv/bin/activate` rewrites $PATH to activate
  new python environment. (Run `deactivate` to terminate
  the environment.)
* `pip install adafruit-circuitpython-ahtx0` installs
  the python libraries we want. See [adafruit documentation](https://github.com/adafruit/Adafruit_CircuitPython_AHTx0).
* `pip freeze > requirements.txt` captures the versions
  of all libraries and dependencies installed by pip so
  that we can recreate the environment in the future
  with little risk of downstream library changes.
  (This step is optional. It is more documentaiton.)
* `python ex1.py` runs our example code.


