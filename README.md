# py_imu_mpu6050

Inertial Measurement Unit (IMU) Driver based on on the [MPU6050](https://invensense.tdk.com/products/motion-tracking/6-axis/mpu-6050/)

# Introduction

This module is able to communicate to the MPU6050 throught I2C. The hardware support is very wide since the code is using Adafruit-Blinka and adafruit-circuitpython-busdevice that provides neccesary configuration for different platform, as shown in the following list:

* FEATHER_HUZZAH
* NODEMCU
* any_raspberry_pi_40_pin
* any_raspberry_pi_cm
* RASPBERRY_PI_A or RASPBERRY_PI_B_REV1 
* RASPBERRY_PI_B_REV2
* BEAGLEBONE_BLACK
* BEAGLEBONE_GREEN
* BEAGLEBONE_BLACK_INDUSTRIAL
* BEAGLEBONE_GREEN_WIRELESS
* BEAGLEBONE_BLACK_WIRELESS
* BEAGLEBONE_POCKETBEAGLE
* ORANGE_PI_PC
* ORANGE_PI_R1
* ORANGE_PI_ZERO
* ORANGE_PI_ONE
* ORANGE_PI_PC_PLUS
* ORANGE_PI_PC_PLUS
* ORANGE_PI_PC_PLUS
* ORANGE_PI_PC_PLUS
* ORANGE_PI_PC_PLUS
* ORANGE_PI_PC_PLUS
* ORANGE_PI_PC_PLUS
* ORANGE_PI_PC_PLUS
* ORANGE_PI_LITE
* ORANGE_PI_PLUS_2E
* GIANT_BOARD
* JETSON_TX1
* JETSON_TX2
* JETSON_XAVIER
* JETSON_NANO
* JETSON_NX
* ODROID_C2
* ODROID_N2
* DRAGONBOARD_410C
* BINHO_NOVA
* MICROCHIP_MCP2221
* SIFIVE_UNLEASHED
* PINE64

# Dependencies

This driver depends on:

"Adafruit-Blinka"
"adafruit-circuitpython-busdevice"
"adafruit-circuitpython-register"

The Hardware is the MPU6050

# Installing from PyPI

On supported GNU/Linux systems like the RRaspberry pi, Beaglebone, Jetson Boards, etc. you can install the driver locally from [PyPI]([pip](https://pip.pypa.io/en/stable/)).
To install for current user:

```bash
pip3 install py-imu-mpu6050
```
To install system-wide (this may be required in some cases):
```bash
sudo pip3 install py-imu-mpu6050
```

To install in a virtual environment in your current project:

```bash
mkdir project-folder-name
cd project-folder-name
python3 -m venv .env
source .env/bin/activate
pip3 install py-imu-mpu6050
```

# Usage Examples

See:
⋅⋅* [examples/MPU6050_SimpleRead_test.py](../examples/MPU6050_SimpleRead_test.py) for a simple read demo.
⋅⋅* [examples/MPU6050_CSV_IMU_test.py](../examples/MPU6050_CSV_IMU_test.py) for a writing IMU data into a csv file.

# Contributing

Contributions are welcome! Please read our Code of Conduct before contributing to help this project stay welcoming.

# Future

Add support to the magnetometer I2C device that can be connected at AUX_SCL and AUX_SDA pins
