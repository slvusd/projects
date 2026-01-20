from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16)
THRUSTER_CHANNEL = 1

print("Setting up ESC...")

# Set the actuation range explicitly for ESCs
# Min=1100μs (full reverse), Max=1900μs (full forward)
kit.continuous_servo[THRUSTER_CHANNEL].set_pulse_width_range(1100, 1900)

# Power OFF your ESC now
print("Disconnect 12V power from ESC")
time.sleep(2)

# Send neutral (throttle=0 should be 1500μs)
kit.continuous_servo[THRUSTER_CHANNEL].throttle = 0
print("Sending neutral signal (1500μs)")
print("Now connect 12V power to ESC")
print("You should hear: 3 beeps, then 1 beep, then 1 more beep (5 total)")

time.sleep(10)

print("\nTrying forward motion...")
kit.continuous_servo[THRUSTER_CHANNEL].throttle = 0.3
time.sleep(3)

print("Stopping...")
kit.continuous_servo[THRUSTER_CHANNEL].throttle = 0
time.sleep(2)

print("Done")

