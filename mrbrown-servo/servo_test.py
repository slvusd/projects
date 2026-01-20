from adafruit_servokit import ServoKit
import time

# 16-channel servo hat
kit = ServoKit(channels=16)

# Servo 15 (index 14 if zero-based? No, ServoKit uses 0-15)
servo_num = 15

# Move from 0 to 100 degrees gradually
for angle in range(0, 180, 5):
    kit.servo[servo_num].angle = angle
    print(f"Moving servo {servo_num} to {angle}°")
    time.sleep(0.2)

for angle in range(180, 0, -5):
    kit.servo[servo_num].angle = angle
    print(f"Moving servo {servo_num} to {angle}°")
    time.sleep(0.2)

print("Done!")
