import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO_PIN = 19  # Example GPIO pin
GPIO.setup(GPIO_PIN, GPIO.OUT)

pwm = GPIO.PWM(GPIO_PIN, 50)  # 50Hz frequency
pwm.start(0)

def set_speed(speed_percent):
    pulse_ms = 1 + (speed_percent / 100)  # 1ms to 2ms
    duty_cycle = ((20 - pulse_ms) / 20) * 100  # Invert and convert to duty cycle
    pwm.ChangeDutyCycle(duty_cycle)

# Example usage
set_speed(75)  # 50% speed
time.sleep(5)
pwm.stop()
GPIO.cleanup()

