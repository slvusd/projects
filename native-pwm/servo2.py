from gpiozero import PWMOutputDevice
import time

# Assume PWM on GPIO 18
pwm = PWMOutputDevice(18)

# Cycle through different duty cycles
pwm.value = 0    # 0% duty cycle
time.sleep(2)
pwm.value = 0.5  # 50% duty cycle
time.sleep(2)
pwm.value = 1    # 100% duty cycle
time.sleep(2)

# Clean up happens automatically when the script ends

