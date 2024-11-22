from flask import Flask, render_template
from gpiozero import LED
from time import sleep

app = Flask(__name__)


@app.route('/')
def home():
	return render_template('index.html')

@app.route('/pin19', methods=['POST'])
def pin19():
	pin19 = LED(19)
	pin19.on()
	sleep(5)
	print("pin19 trigger")
	return "flask is terrible"

@app.route('/pin21', methods=['POST'])
def pin21():
        pin21 = LED(21)
        pin21.off()
        sleep(5)
        print("pin21 trigger")
        return "flask is terrible"

if __name__ == '__main__':
	app.run(host='0.0.0.0')
