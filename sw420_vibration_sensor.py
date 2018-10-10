#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
S185 - Introduction to Single-Board Computers

A Python GPIO interface script that will read the SW-420 Vibration Sensor
Module output.

Execution:
1. Set the executable flag on the script: chmod u+x sw420_vibration_sensor.py
2. Execute with a preceding dot "./", so call ./sw420_vibration_sensor.py
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

# Define the channel(s) that wil be used.  These are the GPIO pins on
# Raspberry Pi that will be used.
#   Input: PIN ?? (GPIO??)
input_channel = 24
#  Output: PIN ?? (GPIO??)
#output_channel_list = []

# Set up the GPIO Channels - INPUT
GPIO.setup(input_channel, GPIO.IN)
# Set up the GPIO Channels - OUTPUT
#GPIO.setup(output_channel_list, GPIO.OUT)

# Define a function that is called when the sensor state changes.
def SensorTrigger(input_channel):
    if GPIO.input(input_channel):
        print ("A vibration has been detected!  Seek Shelter!")
        time.sleep(1)
    else:
        print ("The vibration has stopped.")
        time.sleep(.1)
# EOF: main()

# Define the main() function.
def main():

	# Use the GPIO library interrupts to detect when the sensor channel goes from
	#  1/GPIO.HIGH/True to 0/GPIO.LOW/False or 0/GPIO.LOW/False to 1/GPIO.HIGH/True
	# The bouncetime is the minimum time between two callbacks in milliseconds
	#  (intermediate events will be ignored).
	GPIO.add_event_detect(input_channel, GPIO.BOTH, bouncetime=300)

	# Assign a function to the sensor output channel; execute the function on a
	# state change (1/GPIO.HIGH/True or 0/GPIO.LOW/False ).
	GPIO.add_event_callback(input_channel, SensorTrigger)

	while True:
		# Pause for 1 second to allow the SW-420 sensor to reset.
		time.sleep(1)
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

