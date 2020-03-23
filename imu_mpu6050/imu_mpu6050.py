"""
# Creative Commons Zero v1.0 Universal
#
# Copyright (c) 2020 Romy Bompart
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

======================================================================================
	This class helps the user to use the MPU6050 from Invensense in a
	wide variety of platform listed in the Adafruit_Blinka repository: 
	https://github.com/adafruit/Adafruit_Blinka/blob/master/src/board.py

	Raspberry pi, Beaglebone, Jetson Boards, etc. 

	The code is inspired in the mpu6050-raspberrypi created by Mr Tijn
	https://pypi.org/project/mpu6050-raspberrypi/

	And uses the libraries from Adafruit to make this library more robust and reliable 
=======================================================================================

* Author (s): Romy Bompart
"""
__version__ = "v0.0"
__repo__ = "git@github.com:romybompart/py_imu_mpu6050.git"


from adafruit_register.i2c_struct import UnaryStruct, ROUnaryStruct
from adafruit_bus_device.i2c_device import I2CDevice

class MPU6050:
	"""
	Init the MPU chip at ``address`` on ``i2c_bus``
	
	:param i2c object bus 	-> i2c_bus: The i2c bus to use for the communication 
	:param int type 	-> address: The MPU I2C address
	"""

	""" 
	Class General Variables
	"""
	GRAVITIY_MS2 = 9.80665

	#Registers:
	#General Registers
	PWR_MGMT_1 	= UnaryStruct(0x6B, ">B") 	# 0x6B
	WHO_AM_I	= ROUnaryStruct(0x75, ">B")	# 0X75
	FSYC_DLP_CONFIG = UnaryStruct(0x1A,">B")
	#Temp Sensor Registers
	TEMP_OUTH 	= ROUnaryStruct(0x41, ">b")	# 0x41
	TEMP_OUTL 	= ROUnaryStruct(0x42, ">b")	# 0x41
	#Accelerometer Registers
	ACCEL_CONFIG = UnaryStruct(0x1C, ">B")	# 0x1C
	ACCEL_XOUTH = ROUnaryStruct(0x3B, ">B") # 0x3B
	ACCEL_XOUTL = ROUnaryStruct(0x3C, ">B") # 0x3B   
	ACCEL_YOUTH = ROUnaryStruct(0x3D, ">B")	# 0x3D
	ACCEL_YOUTL = ROUnaryStruct(0x3E, ">B")	# 0x3D
	ACCEL_ZOUTH = ROUnaryStruct(0x3F, ">B")	# 0x3F
	ACCEL_ZOUTL = ROUnaryStruct(0x40, ">B")	# 0x3F
	#Gyroscope Registers
	GYRO_CONFIG = UnaryStruct(0x1B, ">B")	# 0x1B
	GYRO_XOUTH = ROUnaryStruct(0x43, ">B") 	# 0x43
	GYRO_XOUTL = ROUnaryStruct(0x44, ">B") 	# 0x44   
	GYRO_YOUTH = ROUnaryStruct(0x45, ">B")	# 0x45
	GYRO_YOUTL = ROUnaryStruct(0x46, ">B")	# 0x46
	GYRO_ZOUTH = ROUnaryStruct(0x47, ">B")	# 0x47
	GYRO_ZOUTL = ROUnaryStruct(0x48, ">B")	# 0x48

	#Full scale Range ACCEL:
	""" from register 1C bit 4 to 3"""
	ACCEL_RANGE_2G = 0x00
	ACCEL_RANGE_4G = 0x08
	ACCEL_RANGE_8G = 0x10
	ACCEL_RANGE_16G = 0x18

	# LSB Sensitivity
	ACCEL_LSB_SENS_2G = 16384.0
	ACCEL_LSB_SENS_4G = 8192.0
	ACCEL_LSB_SENS_8G = 4096.0
	ACCEL_LSB_SENS_16G = 2048.0

	#Full scale Range GYRO:
	""" from register 1B bit 4 to 3"""
	GYRO_RANGE_250DEG = 0x00
	GYRO_RANGE_500DEG = 0x08
	GYRO_RANGE_1000DEG = 0x10
	GYRO_RANGE_2000DEG = 0x18

    #LSB Sensitivity
	GYRO_LSB_SENS_250DEG = 131.0
	GYRO_LSB_SENS_500DEG = 65.5
	GYRO_LSB_SENS_1000DEG = 32.8
	GYRO_LSB_SENS_2000DEG = 16.4

    #MPU Address
	MPU_ADDRESS = 0x68

	""" 
	Constructor
	"""
	def __init__(self, i2c_bus=None, address=MPU_ADDRESS):

		""" Create an i2c device from the MPU6050"""
		self.i2c = i2c_bus

		if self.i2c == None:
			import busio
			from board import SDA,SCL
			self.i2c = busio.I2C(SCL,SDA)

		self.i2c_device = I2CDevice(self.i2c,address)

		""" Wake up the MPU-6050 since it starts in sleep mode """
		self.wakeup()
		print ( 'MPU already awaked')
		""" verify the accel range and get the accel scale modifier"""
		print ( 'accelerometer range set: {} g'.format(self.read_accel_range()))
		self.accel_scale_modifier = self.get_accel_scale_modifier()
		""" verify the gyro range and get the gyro scale modifier"""
		print ( 'gyroscope range set: {} °/s'.format(self.read_gyro_range()))
		self.gyro_scale_modifier = self.get_gyro_scale_modifier()
		""" configuring the Digital Low Pass Filter """
		#by default: 
		# Bandwith of 21Hz and delay of 8.5ms, Sampling Freq 1KHz -> Accelerometer
		# Bandwith of 20Hz and delay of 8.3ms, Sampling Freq 1KHz -> Gyroscope
		self.filter_sensor = 0x04
		print ('digital filter configure to be: {}'.format(self.filter_sensor))

	""" 
		Class Properties
	"""
	@property
	def whoami(self):
		""" MPU6050 I2C Address """
		return self.WHO_AM_I

	@property
	def get_temp(self):
		""" MPU6050 Temperature """
		H = self.TEMP_OUTH
		L = self.TEMP_OUTL

		raw_temp = self.raw_data_format( ( H << 8 )+ L )

		# Get the actual temperature using the formule given in the
        # MPU-6050 Register Map and Descriptions revision 4.2, page 30
		actual_temp = (raw_temp / 340.0) + 36.53
		return actual_temp

	@property
	def filter_sensor(self):
		"""
		Return the filter sensor
		"""
		return self.FSYC_DLP_CONFIG


	""" Class Setter """
	@filter_sensor.setter
	def filter_sensor(self, filter_value = 0x04):
		"""
		Configuration Register

		In case FYNC pin is used, the bit of the sampling will be reported at 
		any of the following registers. For more information consult MPU-6000-Register
		Map at page 13. 

		EXT_SYNC_SET, bit 5:3, Values:
		000: Input Disable
		001: Temp_Out_L
		010: GYRO_XOUT_L[0] 
		011: GYRO_YOUT_L[0] 
		100: GYRO_ZOUT_L[0]
		101: ACCEL_XOUT_L[0]
		110: ACCEL_YOUT_L[0]
		111: ACCEL_ZOUT_L[0]

		In case to set accelerometer and gyroscope are filtered according to the following
		table. 
		DLPF_CFG, bit 2:0, Values:
					accelerometer 				gyroscope
				Bandwidth	Delays	Fs
		000:	260 Hz 		0	ms 	1KHz 	256 Hz 		0.98ms 	8KHz
		001:	184 Hz 		2	ms 	1KHz 	188 Hz 		1.9	ms 	1KHz
		010:	94	Hz 		3	ms 	1KHz 	98	Hz 		2.8	ms 	1KHz
		011:	44	Hz  	4.9	ms 	1KHz 	42	Hz  	4.8	ms 	1KHz
		100:	21	Hz  	8.5	ms 	1KHz 	20	Hz  	8.3	ms 	1KHz
		101:	10	Hz  	13.8ms	1KHz 	10	Hz  	13.4ms	1KHz
		110:	5	Hz  	19	ms 	1KHz    5	Hz  	18.6ms 	1KHz
		111: 	RESERVED  	   RESERVED     RESERVED   RESERVED 8KHz
		"""
		if ( filter_value < 0x00 and filter_value > 0x07):
			filter_value = 0x04

		self.FSYC_DLP_CONFIG = filter_value 

	"""
		function members
	"""
	def wakeup(self):
		""" waking up the MPU-6050 by writing at the POWER MANAGEMENT REGISTER 1

		Device_Reset, bit 7, values:
		0: Nothing
		1: the device will reset all internal registers to their default values.

		Sleep, bit 6, values:
		0: disables the sleep mode
		1: enables the sleep mode

		Cycle, bit 5 values:
		0: Nothing
		1: The device will cycle between sleep mode and waking up to take a single sample of data
		from active sensors at a rate determined by LP_WAKE_CTRL (register 108)

		Reserverd bit 4, value = 0

		Temp_dis, bit 3, values
		0: Nothing
		1: Disables the temperature sensor

		ClkSel, bit 2:0, values:
		000: Internal 8MHz oscillator 
		001: PLL with X axis gyroscope reference 
		010: PLL with y axis gyroscope reference
		011: PLL with z axis gyroscope reference
		100: PLL with external 32.768kHz reference
		101: PLL with external 19.2MHz reference 
		110: Reserverd
		111: Stops the clock and keeps the timing generator in reset 

		"""
		self.PWR_MGMT_1 = 0x00	# BINARY 01001111

	def sleep(self):
		""" entenring into sleep mode
		Deactivate the internal clock generator and enter into sleep mode
		"""
		self.PWR_MGMT_1 = 0x4F	# BINARY 01001111

	def deinit(self):
		""" stop using the MPU-6050 """
		self.sleep()

	def raw_data_format(self, raw_data):
		""" formating data that comes from the I2C bus"""
		""" This helps to provide the results between -1 and 1 along with the accel or gyro modifier"""
		if (raw_data >= 0x8000):
			raw_data = -((65535 - raw_data) + 1)
		return raw_data

	""" Accelerometer """
	def read_accel_range(self, raw = False):
		"""Reads the range the accelerometer is set to.

		If raw is True, it will return the raw value from the ACCEL_CONFIG
		register
		If raw is False, it will return an integer: -1, 2, 4, 8 or 16. When it
		returns -1 something went wrong.
		"""
		raw_data = self.ACCEL_CONFIG

		if raw is True:
			return raw_data
		elif raw is False:
			if raw_data == self.ACCEL_RANGE_2G:
				return 2
			elif raw_data == self.ACCEL_RANGE_4G:
				return 4
			elif raw_data == self.ACCEL_RANGE_8G:
				return 8
			elif raw_data == self.ACCEL_RANGE_16G:
				return 16
		else:
			return -1

	def set_accel_range(self, value):
		"""
		set accel range
		"""
		cond = (self.ACCEL_RANGE_2G == value) or (self.ACCEL_RANGE_4G == value) \
			   (self.ACCEL_RANGE_8G == value) or (self.ACCEL_RANGE_16G)

		if cond == False:
			value = self.ACCEL_RANGE_2G

		self.ACCEL_CONFIG = value
		self.accel_scale_modifier = self.get_accel_scale_modifier()

	def get_accel_scale_modifier(self):

		accel_range = self.read_accel_range(True)

		if accel_range == self.ACCEL_RANGE_2G:
			accel_scale_modifier = self.ACCEL_LSB_SENS_2G
		elif accel_range == self.ACCEL_RANGE_4G:
			accel_scale_modifier = self.ACCEL_LSB_SENS_4G
		elif accel_range == self.ACCEL_RANGE_8G:
			accel_scale_modifier = self.ACCEL_LSB_SENS_8G
		elif accel_range == self.ACCEL_RANGE_16G:
			accel_scale_modifier = self.ACCEL_LSB_SENS_16G
		else:
			print("Unkown range - accel_scale_modifier set to self.ACCEL_SCALE_MODIFIER_2G")
			accel_scale_modifier = self.ACCEL_LSB_SENS_2G

		return accel_scale_modifier

	def get_accel_data(self, g = False):
		"""Gets and returns the X, Y and Z values from the accelerometer.
		If g is True, it will return the data in g
		If g is False, it will return the data in m/s^2
		Returns a dictionary with the measurement results.
		"""
		XH = self.ACCEL_XOUTH
		XL = self.ACCEL_XOUTL
		YH = self.ACCEL_YOUTH
		YL = self.ACCEL_YOUTL
		ZH = self.ACCEL_ZOUTH
		ZL = self.ACCEL_ZOUTL

		x = self.raw_data_format(( XH << 8 ) + XL)	
		y = self.raw_data_format(( YH << 8 ) + YL)	
		z = self.raw_data_format(( ZH << 8 ) + ZL)	

		x = x / self.accel_scale_modifier
		y = y / self.accel_scale_modifier
		z = z / self.accel_scale_modifier

		if g is False:
			x = x * self.GRAVITIY_MS2
			y = y * self.GRAVITIY_MS2
			z = z * self.GRAVITIY_MS2

		return {'x': x, 'y': y, 'z': z}

	""" Gyroscope """
	def read_gyro_range(self, raw = False):
	    """Reads the range the gyroscope is set to.
	    If raw is True, it will return the raw value from the GYRO_CONFIG
	    register.
	    If raw is False, it will return 250, 500, 1000, 2000 or -1. If the
	    returned value is equal to -1 something went wrong.
	    """
	    raw_data = self.GYRO_CONFIG

	    if raw is True:
	        return raw_data
	    elif raw is False:
	        if raw_data == self.GYRO_RANGE_250DEG:
	            return 250
	        elif raw_data == self.GYRO_RANGE_500DEG:
	            return 500
	        elif raw_data == self.GYRO_RANGE_1000DEG:
	            return 1000
	        elif raw_data == self.GYRO_RANGE_2000DEG:
	            return 2000
	        else:
	            return -1

	def set_gyro_range(self, value):
		"""
		set gyro range
		"""
		cond = (self.GYRO_RANGE_250DEG == value) or (self.GYRO_RANGE_500DEG == value) \
			   (self.GYRO_RANGE_1000DEG == value) or (self.GYRO_RANGE_2000DEG)

		if cond == False:
			value = self.GYRO_RANGE_250DEG

		self.GYRO_CONFIG = value
		self.gyro_scale_modifier = self.get_gyro_scale_modifier()

	def get_gyro_scale_modifier(self):
		"""
		Get gyro scale modifier from reading the gyro range
		"""
		gyro_range = self.read_gyro_range(True)

		if gyro_range == self.GYRO_RANGE_250DEG:
			gyro_scale_modifier = self.GYRO_LSB_SENS_250DEG
		elif gyro_range == self.GYRO_RANGE_500DEG:
			gyro_scale_modifier = self.GYRO_LSB_SENS_500DEG
		elif gyro_range == self.GYRO_RANGE_1000DEG:
			gyro_scale_modifier = self.GYRO_LSB_SENS_1000DEG
		elif gyro_range == self.GYRO_RANGE_2000DEG:
			gyro_scale_modifier = self.GYRO_LSB_SENS_2000DEG
		else:
			print("Unkown range - gyro_scale_modifier set to self.GYRO_LSB_SENS_250DEG")
			gyro_scale_modifier = self.GYRO_LSB_SENS_250DEG

		return gyro_scale_modifier

	def get_gyro_data(self):
		"""
		Gets and returns the X, Y and Z values from the gyroscope.
		"""
		XH = self.GYRO_XOUTH
		XL = self.GYRO_XOUTL
		YH = self.GYRO_YOUTH
		YL = self.GYRO_YOUTL
		ZH = self.GYRO_ZOUTH
		ZL = self.GYRO_ZOUTL

		x = self.raw_data_format(( XH << 8 ) + XL)	
		y = self.raw_data_format(( YH << 8 ) + YL)	
		z = self.raw_data_format(( ZH << 8 ) + ZL)	

		x = x / self.gyro_scale_modifier
		y = y / self.gyro_scale_modifier
		z = z / self.gyro_scale_modifier

		return {'x': x, 'y': y, 'z': z}

	"""
		magic methos helps to make easy the use of with
	"""
	def __enter__(self):
		""" to make easy the use of with """
		return self

	def __exit__(self, exceptio_typ, exception_value, traceback):
		""" to make easy the use of with """
		self.deinit()

""" __end__ """
