from flask import Flask, render_template
from gpiozero import LED
from time import sleep
from board import I2C
from adafruit_ahtx0 import AHTx0
from threading import Lock

app = Flask(__name__)

#sets up thermometer
i2c = I2C()
thermometer = AHTx0(i2c)
temper = thermometer.temperature

def control(command):
	mutex = Lock()
	mutex.aquire()

	pin17 = LED(17)
	pin27 = LED(27)

	if command == 1:
		pin17.on()
		print("pin17 (open) trigger")
		sleep(5)
	elif command == -1:
		pin27.on()
		print("pin27 (close) trigger")
		sleep(5)

	mutex.release()
	return

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/pin17', methods=['POST'])
def pin17():
	control(1)
	return '', 200

@app.route('/pin27', methods=['POST'])
def pin27():
	control(-1)
	return '', 200

@app.route('/temper', methods=['GET'])
def temper():
	temper = thermometer.temperature
	return {"temper": temper}

if __name__ == '__main__':
	app.run(host='0.0.0.0')
