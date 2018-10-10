#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
S185 - Introduction to Single-Board Computers

A Python GPIO interface script file for the TTP223 Digital Touch Sensor Module.

This version of the Python script will only print an output once each time the
sensor detects a touch.

Execution:
1. Set the executable flag on the script: chmod u+x ttp223_touch_sensor_trigger.py
2. Execute with a preceding dot "./", so call ./ttp223_touch_sensor_trigger.py
"""

# Import required modules.
import os
import sys
import argparse
import time

# Import the RPi.GPIO module/library.  This is the package that provides a GPIO
# interface.
try:
	import RPi.GPIO as GPIO
except RuntimeError:
	print("Error importing RPi.GPIO!")

# Select the GPIO numbering scheme.
# Refer to the GPIO pins by the channel numbers on the
#  Broadcom SOC.
GPIO.setmode(GPIO.BCM)
# - or -
# Refer to the GPIO pins by the BOARD numbering system.
#  This refers to the pin numbers on the P1 header of
#  the Raspberry Pi board.
#GPIO.setmode(GPIO.BOARD)

# Define the channel(s) that will be used. These are the GPIO pins on
# Raspberry Pi that will be used.
#   Input: PIN ?? (GPIO??)
input_channel_list  = [23]
#  Output: PIN ?? (GPIO??)
#output_channel_list = []

# Set up the GPIO Channels - INPUT
GPIO.setup(input_channel_list, GPIO.IN)
# Set up the GPIO Channels - OUTPUT
#GPIO.setup(output_channel_list, GPIO.OUT)

# Define the main() function.
def main():
	# Set the variable that is used to check if the sensor has already been touched.
	SensorAlreadyTouched = False

	while True:
		# Get/Read the state of the touch sensor.
		# 1/GPIO.HIGH/True : Touched
		# 0/GPIO.LOW/False : Not touched.
		SensorState =  GPIO.input(input_channel_list[0])

		# Check the current touch sensor state with the previous touch sensor
		# state.  If they are different, print/display a message.
		if SensorState and not SensorAlreadyTouched:
			print ("The sensor has been triggered.")

		# Save the state of the touch sensor.
		SensorAlreadyTouched = SensorState

		time.sleep(0.1)
# EOF: main()

# ------------------------------------------------- BEGIN EXECUTION HERE --
if __name__ == '__main__':
	try:
		# Execute code in here first.
		# if an exception is raised, continue to check except blocks.
		# ~~~~~
		# Invoke the main function.
		main()
	except KeyboardInterrupt:
		# If the exception is of this type...
		# Execute this code and continue to 'finally' block.
		# ~~~~~
		# Raised when the user interrupts program execution,
		#	usually by pressing Ctrl+c.
		pass
	finally:
		# No matter what has happened previously, or whether an
		# exception was thrown, execute this code as the program ends.
		# ~~~~~
		print("Cleaning up GPIO pins...")
		# Reset the status of the GPIO pins.
		# NOTE: This will only clean up GPIO channels that your script
		#	has used. This also clears the pin numbering system in use.
		GPIO.cleanup()
