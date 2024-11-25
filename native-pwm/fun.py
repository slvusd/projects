import pi_servo_hat
import time
import sys

hat = pi_servo_hat.PiServoHat()

hat.restart()

hat.set_pwm_frequency(50)
hat.set_duty_cycle(0, 82) # 20 ms
hat.set_pulse_time(1, 2)

