"""
	Simple code to read data from the temperature sensor, accelerometer and gyroscope sensors
	inside of MPU6050

	The propertie whoami provides the i2c address of the device
"""

from board import SDA,SCL
from imu_mpu6050 import MPU6050
import busio

import time

def main():
	i2c = busio.I2C(SCL,SDA)
	IMU = MPU6050(i2c)

	print ("Identification 0x{:X} ".format(IMU.whoami))


	i = 0
	while ( i <10 ):
		print ("Temperature [c]: {}".format(IMU.get_temp))
		time.sleep(1)
		i+=1

	i = 0
	while ( i <10 ):
		print ("acelerometer data [g]: {}".format(IMU.get_accel_data(g=True)))
		time.sleep(0.1)
		i+=1

	i= 0
	while ( i <10 ):
		print ("gyroscope data [°/s]: {}".format(IMU.get_gyro_data()))
		time.sleep(0.1)
		i+=1


if __name__ == '__main__':
	main()
