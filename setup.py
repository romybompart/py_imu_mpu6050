"""
    A setup based on setuptools
    see: https://packaging.python.org/tutorials/packaging-projects/

"""

import setuptools

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md")) as f:
    long_description = f.read()

setuptools.setup(
    name="py-imu-mpu6050", # packagename sam as container folder
    use_scm_version = True, 
    setup_requires=["setuptools_scm"],
    description=" Inertial Measurement Unit (IMU) Driver based on on the MPU6050",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # The project's main homepage.
    url="https://github.com/romybompart/py_imu_mpu6050",
    # Author details
    author="Romy Bompart",
    author_email="romybompart@gmail.com",
    install_requires=[
        "Adafruit-Blinka",
        "adafruit-circuitpython-busdevice",
        "adafruit-circuitpython-register",
    ],
    # Choose your license
    license="Creative Commons Zero v1.0 Universal",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Hardware",
        "License :: OSI Approved :: Common Development and Distribution License 1.0 (CDDL-1.0)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    # What does your project relate to?
    keywords="IMU MPU6050 i2c hardware python jetsonnano raspberrypi adafruit",
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=["imu_mpu6050"],
)
