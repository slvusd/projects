from gpiozero import PWMOutputDevice
import time

pwm = PWMOutputDevice(18,frequency=50,active_high=False)

pwm.value = 0.075 # off
print("stop")
time.sleep(4)
pwm.value = 0.065 # backward
print("back")
time.sleep(4)
pwm.value = 0.055
print("fwd")
time.sleep(4)

pwm.close()
