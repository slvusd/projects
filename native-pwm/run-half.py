from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
import signal
from time import sleep

# Use pigpio for better PWM timing
factory = PiGPIOFactory()

# Create servo object with custom pulse widths for ESC
# min_pulse_width is full reverse (1ms)
# max_pulse_width is full forward (2ms)
# mid_pulse_width is neutral (1.5ms)
esc = Servo(
    18,  # GPIO18 (Pin 12)
    pin_factory=factory,
    min_pulse_width=0.001,    # 1ms
    max_pulse_width=0.002,    # 2ms
    frame_width=0.020         # 50Hz -> 20ms frame
)

def cleanup():
    print('\nStopping motor and cleaning up...')
    esc.detach()  # This stops PWM output

def signal_handler(sig, frame):
    cleanup()
    exit(0)

if __name__ == "__main__":
    try:
        # Register signal handler for clean exit
        signal.signal(signal.SIGINT, signal_handler)
        
        # Start at neutral position (value 0)
        print("Initializing ESC...")
        esc.value = 0
        sleep(2)  # Give ESC time to initialize
        
        # Set to half speed forward (value 0.5)
        # GPIOZero maps -1 to +1 to the full pulse width range
        # So 0.5 is halfway between neutral and full forward
        print("Running motor at 1/2 speed forward. Press CTRL+C to stop.")
        esc.value = 0.5
        
        # Keep program running until CTRL+C
        signal.pause()
        
    except Exception as e:
        print(f"Error occurred: {e}")
        cleanup()

