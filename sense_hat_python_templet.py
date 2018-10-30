#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
S185 - Introduction to Single-Board Computers

A simple python Sense HAT interface script template.

Execution:
1. Set the executable flag on the script: chmod u+x sense_hat_python_templet.py
2. Execute with a preceding dot "./", so call ./sense_hat_python_templet.py
"""

# Import required modules.
import os
import sys
import argparse
import time

# Import the Sense HAT module.
try:
	import sense_hat
except RuntimeError:
	print("Error importing Sense HAT module!")

# Instantiate the Sense HAT object.
sense = sense_hat.SenseHat()

# Define the main() function.
def main():
	# Your code goes here.
	pass
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
