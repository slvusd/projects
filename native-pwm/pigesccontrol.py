from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
import signal
from time import sleep

# Using pigpio for hardware-timed PWM - this is important for smooth operation
factory = PiGPIOFactory()

# Create servo object with precise hardware timing
esc = Servo(
    18,                        # GPIO18 (Pin 12)
    min_pulse_width=0.001,     # 1ms
    max_pulse_width=0.002,     # 2ms
    frame_width=0.020,         # 20ms (50Hz)
    pin_factory=factory        # Use hardware PWM timing
)

def stop_motor():
    print('\nStopping motor...')
    esc.value = 0
    sleep(0.5)
    esc.detach()

def handle_exit(sig, frame):
    stop_motor()
    exit(0)

if __name__ == "__main__":
    try:
        signal.signal(signal.SIGINT, handle_exit)
        
        print("Initializing ESC...")
        esc.value = 0  # Start at neutral
        sleep(2)
        
        print("Running motor at 1/2 speed forward...")
        esc.value = 0.5
        print("Press Ctrl+C to stop the motor.")
        
        signal.pause()
        
    except Exception as e:
        print(f"Error occurred: {e}")
        stop_motor()

