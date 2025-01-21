from flask import Flask, render_template
from gpiozero import LED
from time import sleep
from board import I2C
from adafruit_ahtx0 import AHTx0

app = Flask(__name__)

#sets up thermometer
i2c = I2C()
thermometer = AHTx0(i2c)
temper = thermometer.temperature

@app.route('/')
def index():
	return render_template('index.html', temper=temper)

@app.route('/pin17', methods=['POST'])
def pin17():
	pin17 = LED(17)
	pin17.on()
	sleep(5)
	print("pin17 (open) trigger")
	return "flask is terrible"

@app.route('/pin27', methods=['POST'])
def pin27():
        pin27 = LED(27)
        pin27.on()
        sleep(5)
        print("pin27 (close) trigger")
        return "flask is terrible"

if __name__ == '__main__':
	app.run(host='0.0.0.0')
