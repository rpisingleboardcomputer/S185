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
1. Set the executable flag on the script: chmod u+x sense_hat_imu_sensor_gs.py
2. Execute with a preceding dot "./", so call ./sense_hat_imu_sensor_gs.py
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
	# RED: Define the RGB color
	red = (255, 0, 0)
	# !!!Clemson!!! Orange: Define the RGB color
	orange = (246, 103, 51)

	# Sensitive factor
	gamma = 0.9

	while True:
		# Read the raw x, y and z axis accelerometer data.
		# The values represent the acceleration intensity of the axis in Gs.
		# i.e., Read the amount of G-force acting on each axis (x, y, z).
		# If any axis has ±1G, then you know that axis is pointing downwards.
		acceleration = sense.get_accelerometer_raw()
		x = acceleration['x']
		y = acceleration['y']
		z = acceleration['z']

		print("X: {0} \t Y: {1} \t Z: {2}".format(round(x,3), round(y,3), round(z,3)))

		# The direction of the acceleration intensity of the axis for the
		#  Sense HAT is not important.
		x = abs(x)
		y = abs(y)
		z = abs(z)

		# For G-forces acting on the axis (x, y, or z), Identify a force is being
		#  encountered on LED matrix.
		# if x > (1+gamma) or y > (1+gamma) or z > (1+gamma):
			# sense.show_letter("+", orange)
		# else:
			# sense.clear()

		# For G-forces acting on an axis (x, y, or z), Identify the axis on the
		#  LED matrix.
		if x > (1+gamma):
			sense.show_letter("X", orange)
		elif y > (1+gamma):
			sense.show_letter("Y", orange)
		elif z > (1+gamma):
			sense.show_letter("Z", orange)
		else:
			sense.clear()
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
