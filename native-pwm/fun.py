# Eric Brown
# There is something wrong with the docs.
# But playing with values here, maybe it can be figured out.
import pi_servo_hat
import time
import sys

hat = pi_servo_hat.PiServoHat()

hat.restart()

hat.set_pwm_frequency(50)
hat.set_duty_cycle(0, 82) # 20 ms
hat.set_pulse_time(1, 2)

# Map pulse width in microseconds to servo position (-1.0 to 1.0)
def pulse_width_to_position(pulse_width_us):
    """
    Convert pulse width (in microseconds) to position for pi_servo_hat.
    1000 µs maps to -1.0, 2000 µs maps to 1.0, and 1500 µs maps to 0.0.
    """
    position = (pulse_width_us - 1500) / 500.0 * 360 / (2*3.1415)
    print(f"Pulse: {pulse_width_us}  Position: {position}")
    return position

hat.move_servo_position(0, pulse_width_to_position(2000))
time.sleep(5)
hat.move_servo_position(0, 40)
time.sleep(5)

for i in range(1, 180):
    print(i)
    hat.move_servo_position(0, i)
    time.sleep(.2)

#hat.move_servo_position(0, pulse_width_to_position(1750))
#time.sleep(5)

