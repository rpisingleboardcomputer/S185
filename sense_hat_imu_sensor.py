#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
S185 - Introduction to Single-Board Computers

Read data from the IMU sensor on the Sense HAT.  This sensor is
considered to be a 9-DOF (degrees of freedom) sensor.
 - Gyroscope
 - Accelerometer
 - Magnetometer (compass)


Execution:
1. Set the executable flag on the script: chmod u+x sense_hat_imu_sensor.py
2. Execute with a preceding dot "./", so call ./sense_hat_imu_sensor.py
"""

# Import required modules.
import os
import sys
import argparse
import time
import random

# Import the Sense HAT module.
try:
	import sense_hat
except RuntimeError:
	print("Error importing Sense HAT module!")

# Instantiate the Sense HAT object.
sense = sense_hat.SenseHat()

# Define the main() function.
def main():
	while True:
		# Gets the current orientation in degrees
		#	using the aircraft principal axes of pitch, roll and yaw.
		orientation_degrees = sense.get_orientation()
		pitch	= round(orientation_degrees["pitch"], 3)
		roll 	= round(orientation_degrees["roll"], 3)
		yaw 	= round(orientation_degrees["yaw"], 3)
		print("Pitch: {0} \t Roll: {1} \t Yaw: {2}".format(pitch, roll, yaw))
# EOF: main()

# ------------------------------------------------- BEGIN EXECUTION HERE --
if __name__ == '__main__':
	try:
		# Execute code in here first.
		# If an exception is raised, continue to check except blocks.
		# ~~~~~
		# Invoke the main function.
		main()
	except KeyboardInterrupt:
		# If the exception is of this type...
		# Execute this code and continue to finally block.
		# ~~~~~
		# Raised when the user interrupts program execution, usually by
		#  pressing Ctrl+c.
		# ~~~~~
		# Sets the entire LED matrix to a single color, defaults to
		#  blank/off.
		sense.clear()
	finally:
		# No matter what has happened previously, or whether an
		# exception was thrown, execute this code as the program ends.
		# ~~~~~
		# Sets the entire LED matrix to a single color, defaults to
		#  blank/off.
		sense.clear()