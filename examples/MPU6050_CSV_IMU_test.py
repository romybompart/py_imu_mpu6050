from board import SDA,SCL
from imu_mpu6050 import MPU6050
import busio
import os

import time

def main():
	i2c = busio.I2C(SCL,SDA)
	IMU = MPU6050(i2c)

	print ("Identification 0x{:X} ".format(IMU.whoami))

	outfile = 'data-alt.csv'
	outsize = 100000 #Bytes
	chunksize = 10
	data = []
	with open(outfile, 'w+') as csvfile:
		csvfile.writelines(" {:5s} , {:5s} , {:5s} , {:5s} , {:5s} , {:5s} , {:5s}, \n".format(" Temp", "Xa","Ya","Za","Xg","Yg","Zg"))
		while (os.path.getsize(outfile)) < outsize: 
			data.append(IMU.get_temp)
			data.append(IMU.get_accel_data(g=True))
			data.append(IMU.get_gyro_data())

			if len(data) == chunksize*3:
				y=0
				for y in range ( 0, len(data) , 3):
					csvfile.writelines(" {0:.5f} , {d1[x]} , {d1[y]} , {d1[z]} , {d2[x]} , {d2[y]} , {d2[z]}, \n"\
										.format(data[y],d1=data[y+1],d2=data[y+2])) 
				data.clear()

			time.sleep(0.1)


if __name__ == '__main__':
	main()