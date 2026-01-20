from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16)
kit.frequency = 50  # 50 Hz

esc_channel = 1
kit.servo[esc_channel].set_pulse_width_range(1000, 2000)

def esc_write(channel, pulse_us):
    min_us = 1000
    max_us = 2000
    pulse_us = max(min_us, min(max_us, pulse_us))  # clamp
    angle = (pulse_us - min_us) / (max_us - min_us) * 180
    kit.servo[channel].angle = angle

# --- ESC Initialization Sequence ---

# 1️⃣ Make sure ESC is powered
# Connect power to ESC now. Pi does not supply motor power.

# 2️⃣ Send full reverse (1000 µs) for 2 sec
esc_write(esc_channel, 1000)
print("Sending 1000 µs (full reverse) to arm ESC")
time.sleep(2)

# 3️⃣ Send neutral (1500 µs) for 2 sec
esc_write(esc_channel, 1500)
print("Sending 1500 µs (neutral) to complete arming")
time.sleep(2)

# 4️⃣ Now ESC should beep 3 times and be ready
print("ESC should now be armed and ready")
