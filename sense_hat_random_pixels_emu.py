#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
S185 - Introduction to Single-Board Computers

Randomly light pixels in the LED matrix with a random color on the
Sense HAT emulator.

Execution:
1. Set the executable flag on the script: chmod u+x sense_hat_random_pixels_emu.py
2. Execute with a preceding dot "./", so call ./sense_hat_random_pixels_emu.py
"""

# Import required modules.
import os
import sys
import argparse
import time
import random

# Import the Sense HAT module.
try:
	from sense_emu import SenseHat
except RuntimeError:
	print("Error importing Sense HAT emulator module!")

# Instantiate the Sense HAT object.
sense = sense_hat.SenseHat()

# Define the main() function.
def main():
	# Set the LED matrix to the low light mode.
	sense.low_light = True

	while True:
		# Generate a random x and y position
		#	x: 0 is on the left, 7 on the right.
		#	y: 0 is at the top, 7 at the bottom.
		x = random.randint(0, 7)
		y = random.randint(0, 7)
		# Generate a random RGB (red, green, blue) color. Each color value must
		#  be an integer between 0 and 255.
		r = random.randint(0, 255)
		g = random.randint(0, 255)
		b = random.randint(0, 255)
		pixel_color = (r, g, b)
		# Set an individual LED matrix pixel at the specified (x,y) coordinate,
		#	to the specified RGB (red, green, blue) color.
		#sense.set_pixel(x, y, r, g, b)
		sense.set_pixel(x, y, pixel_color)
		time.sleep(0.01)
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
