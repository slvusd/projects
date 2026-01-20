from adafruit_servokit import ServoKit
import time

# --- Setup ---
kit = ServoKit(channels=16)
kit.frequency = 50  # 50 Hz for ESC
esc_channel = 1     # adjust if your ESC is on a different channel
kit.servo[esc_channel].set_pulse_width_range(1000, 2000)

# --- Helper function: send microseconds to ESC ---
def esc_write(channel, pulse_us):
    min_us = 1000
    max_us = 2000
    pulse_us = max(min_us, min(max_us, pulse_us))  # clamp
    angle = (pulse_us - min_us) / (max_us - min_us) * 180
    kit.servo[channel].angle = angle

# --- Trial sequences ---
sequences = [
    ("Neutral only", [1500]),           # just neutral
    ("Full reverse → neutral", [1000, 1500]),
    ("Full reverse only", [1000]),
    ("Full forward → neutral", [2000, 1500])
]

print("Starting ESC arming trials. Make sure prop is disconnected!")
time.sleep(2)

for name, pulses in sequences:
    print(f"\nTrying sequence: {name}")
    for pulse in pulses:
        print(f"  Sending {pulse} µs")
        esc_write(esc_channel, pulse)
        time.sleep(2)  # hold each pulse long enough for ESC to detect it
    print("  Done with sequence, wait 2 sec before next")
    time.sleep(2)

print("\nAll sequences sent. Did your ESC beep?")
