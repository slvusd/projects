from slvrov_tools.pca9685 import PCA9685
from time import sleep

driver = PCA9685(50)


for i in range(0, 51):
	pwm = 1000 + i * 20
	print(pwm)
	driver.write_duty_cycle(15,pwm) 
	sleep(0.1)
driver.write_duty_cycle(15, 1500)
