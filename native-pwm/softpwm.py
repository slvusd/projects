from gpiozero import PWMOutputDevice
from time import sleep

# Define the GPIO pin for PWM output
pwm_pin = 26
esc = PWMOutputDevice(pwm_pin, frequency=50)  # 50 Hz frequency

def arm_esc():
    # Send minimum throttle signal to arm the ESC
    esc.value = 0  # 0% duty cycle (1ms pulse)
    sleep(2)       # Wait for 2 seconds
    esc.value = 1  # 100% duty cycle (2ms pulse)
    sleep(2)       # Wait for 2 seconds
    esc.value = 0  # Return to minimum throttle
    print("ESC armed")

def set_throttle(angle):
    # Ensure angle is within valid range (40 to 140)
    if angle < 40:
        angle = 40
    elif angle > 140:
        angle = 140

    # Map angle (40-140) to duty cycle (0-1)
    # - Angle 40 corresponds to about a 10% duty cycle (1ms)
    # - Angle 90 corresponds to about a 50% duty cycle (1.5ms)
    # - Angle 140 corresponds to about a 90% duty cycle (2ms)
    
    duty_cycle = (angle - 40) / (140 - 40) * (0.9) + 0.1
    esc.value = duty_cycle

try:
    arm_esc()          # Arm the ESC first
    print("Setting throttle to full forward...")
    set_throttle(40)  # Full forward (minimum throttle)
    sleep(5)

    print("Setting throttle to stop...")
    set_throttle(90)  # Stop (neutral position)
    sleep(5)

    print("Setting throttle to full reverse...")
    set_throttle(140) # Full reverse (maximum throttle)
    sleep(5)

finally:
    esc.value = 0     # Ensure the ESC is stopped

