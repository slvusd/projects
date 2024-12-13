from flask import Flask, render_template
from gpiozero import LED
from time import sleep
from board import I2C
from adafruit_ahtx0 import AHTx0

app = Flask(__name__)


@app.route('/')
def home():
	return render_template('index.html')

@app.route('/pin17', methods=['POST'])
def pin17():
	pin17 = LED(17)
	pin17.on()
	sleep(5)
	print("pin17 (on) trigger")
	return "flask is terrible"

@app.route('/pin27', methods=['POST'])
def pin27():
        pin27 = LED(27)
        pin27.on()
        sleep(5)
        print("pin27 (off) trigger")
        return "flask is terrible"

@app.route('')

if __name__ == '__main__':
	app.run(host='0.0.0.0')
