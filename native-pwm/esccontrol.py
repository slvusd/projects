from gpiozero import Servo
from gpiozero.pins.native import NativePin
import signal
from time import sleep

# Create servo object with explicit pulse widths
esc = Servo(
    18,                        # GPIO18 (Pin 12)
    min_pulse_width=0.001,     # 1ms for full reverse
    max_pulse_width=0.002,     # 2ms for full forward
    frame_width=0.020          # 20ms frame (50Hz)
)

def stop_motor():
    print('\nStopping motor...')
    # 1.5ms pulse for neutral
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
        print("Setting neutral position (1.5ms pulse)")
        esc.value = 0
        sleep(2)
        
        print("\nCurrent settings:")
        print("- Frequency: 50Hz (20ms period)")
        print("- Neutral: 1.5ms pulse")
        print("- Half forward: 1.75ms pulse")
        print("- Signal pin: GPIO18 (Physical Pin 12)")
        
        print("\nRunning motor at 1/2 speed forward...")
        esc.value = 0.5  # 1.75ms pulse (halfway between 1.5ms and 2ms)
        
        print("Press Ctrl+C to stop the motor.")
        signal.pause()
        
    except Exception as e:
        print(f"Something went wrong: {e}")
        stop_motor()

