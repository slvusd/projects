from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
import signal
from time import sleep

# Using pigpio for hardware-timed PWM
factory = PiGPIOFactory()

# Global flag for clean exit
running = True

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
    global running
    running = False

def initialize_esc():
    print("Starting ESC initialization sequence...")
    print("Setting neutral position...")
    esc.value = 0
    sleep(2)

if __name__ == "__main__":
    try:
        # Set up clean exit when Ctrl+C is pressed
        signal.signal(signal.SIGINT, handle_exit)
        
        # Run initialization sequence
        initialize_esc()
        
        print("Running motor at 1/2 speed forward...")
        print("Press Ctrl+C to stop the motor.")
        esc.value = 0.5
        
        # Keep the program running and actively maintaining the PWM signal
        while running:
            sleep(0.1)  # Small delay to prevent CPU hogging
            
        # Clean up when loop exits
        stop_motor()
        
    except Exception as e:
        print(f"Error occurred: {e}")
        stop_motor()

