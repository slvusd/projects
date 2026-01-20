from adafruit_servokit import ServoKit
import time

# Initialize the servo hat
kit = ServoKit(channels=16)

# Which channel is your T200 connected to?
THRUSTER_CHANNEL = 1

print("Starting thruster test...")

# IMPORTANT: ESCs need continuous_servo, not servo
# Throttle range is -1 to +1, where 0 is stopped

# Start at neutral (stopped)
kit.continuous_servo[THRUSTER_CHANNEL].throttle = 0
print("Neutral - thruster should be stopped")
time.sleep(3)

# Slow forward
kit.continuous_servo[THRUSTER_CHANNEL].throttle = 0.2
print("Slow forward (20%)")
time.sleep(3)

# Medium forward
kit.continuous_servo[THRUSTER_CHANNEL].throttle = 0.5
print("Medium forward (50%)")
time.sleep(3)

# Back to neutral (stopped)
kit.continuous_servo[THRUSTER_CHANNEL].throttle = 0
print("Stopped")
time.sleep(2)

# Try reverse
kit.continuous_servo[THRUSTER_CHANNEL].throttle = -0.3
print("Reverse (30%)")
time.sleep(3)

# Stop
kit.continuous_servo[THRUSTER_CHANNEL].throttle = 0
print("Test complete - stopped")

