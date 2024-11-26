import pigpio
import time

# Set up pigpio
pi = pigpio.pi()  # Connect to local pigpio daemon

# Define GPIO pin connected to ESC signal wire
ESC_PIN = 18  # Change this to your actual GPIO pin

# Function to set duty cycle based on percentage
def set_esc_duty_cycle(duty_cycle):
    # Convert duty cycle (0.065, 0.075, 0.085) to pulse width in microseconds
    # Duty cycle at 50 Hz means a period of 20 ms (20000 µs)
    pulse_width = int(duty_cycle * 20000)  # Convert to microseconds
    pi.set_servo_pulsewidth(ESC_PIN, pulse_width)

try:
    # Test duty cycles for 4 seconds each
    duty_cycles = [0.065, 0.075, 0.085]
    
    for duty_cycle in duty_cycles:
        print(f"Setting duty cycle to {duty_cycle}")
        set_esc_duty_cycle(duty_cycle)
        time.sleep(4)  # Wait for 4 seconds at each duty cycle

finally:
    # Cleanup
    pi.set_servo_pulsewidth(ESC_PIN, 0)  # Stop sending signal
    pi.stop()  # Disconnect from pigpio daemon

