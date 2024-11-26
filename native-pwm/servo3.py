from gpiozero import PWMOutputDevice
import time

pwm = PWMOutputDevice(18,frequency=50)

try:
    for _ in range(5):  # Repeat 5 times
        # Ramp up
        for value in [x/100 for x in range(0, 21, 10)]:
            pwm.value = value
            print(value)
            time.sleep(0.5)
        
        # Ramp down
        for value in [x/100 for x in range(100, -1, -10)]:
            pwm.value = value
            print(value)
            time.sleep(0.1)

except KeyboardInterrupt:
    pass
finally:
    pwm.close()

