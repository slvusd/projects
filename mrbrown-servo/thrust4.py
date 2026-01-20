from adafruit_servokit import ServoKit
import time

# Initialize the servo hat
kit = ServoKit(channels=16)

# Which channel is your T200 connected to? (0-15)
THRUSTER_CHANNEL = 0

print("Starting thruster test...")

# Start at neutral (stopped)
kit.servo[THRUSTER_CHANNEL].angle = 90
print("Neutral - thruster should be stopped")
time.sleep(3)

# Slow forward
kit.servo[THRUSTER_CHANNEL].angle = 110
print("Slow forward")
time.sleep(3)

# Medium forward
kit.servo[THRUSTER_CHANNEL].angle = 130
print("Medium forward")
time.sleep(3)

# Back to neutral (stopped)
kit.servo[THRUSTER_CHANNEL].angle = 90
print("Stopped")
time.sleep(2)

print("Test complete")

