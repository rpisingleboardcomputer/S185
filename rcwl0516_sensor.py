#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
S185 - Introduction to Single-Board Computers

A Python GPIO interface script for the RCWL-0516 Microwave Radar Motion Sensor.

Execution:
1. Set the executable flag on the script: chmod u+x rcwl0516_sensor.py
2. Execute with a preceding dot "./", so call ./rcwl0516_sensor.py
"""

#  Import required modules.
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
# Refer to the GPIO pins by the channel numbers on the Broadcom SOC.
GPIO.setmode(GPIO.BCM)
# - or -
# Refer to the GPIO pins by the BOARD numbering system.
#  This refers to the pin numbers on the P1 header of the Raspberry Pi board.
#GPIO.setmode(GPIO.BOARD)

# Define the channel(s) that wil be used.  These are the GPIO pins on
# Raspberry Pi that will be used.
#   Input: PIN 22 (GPIO25)
input_channel = 25
#  Output: PIN ?? (GPIO??)
#output_channel_list = []

# Set up the GPIO Channels - INPUT
GPIO.setup(input_channel, GPIO.IN)
# Set up the GPIO Channels - OUTPUT
#GPIO.setup(output_channel_list, GPIO.OUT)

# Define a callback function
def SensorTrigger(input_channel):
	print( "RCWL-0516 Sensor Motion Triggered! " + time.strftime("%H:%M:%S") )

# Define the main() function.
def main():
	# For the input pin connected to the RCWL-0516 sensor, on the
	#	rising edge detection on a channel, trigger a callback function.
	#GPIO.add_event_detect(input_channel, GPIO.RISING, callback=SensorTrigger)
	GPIO.add_event_detect(input_channel, GPIO.RISING)

	# Assign a function to the sensor output channel; execute the function on a
	# state change.
	GPIO.add_event_callback(input_channel, SensorTrigger)

	while True:
		# Pause.  The sensor has a response time: 2 seconds.  The will allow the
		#  sensor to reset.
		#time.sleep(2)
		pass
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
		# Execute this code and continue to finally block.
		# ~~~~~
		# Raised when the user interrupts program execution,
		#	usually by pressing Ctrl+c.
		pass
	finally:
		# No matter what has happened previously, or whether an
		# exception was thrown, execute this code as the program ends.
		# ~~~~~
		print("Cleaning up GPIO Pins...")
		# Reset the status of the GPIO pins.
		# NOTE: This will only clean up GPIO channels that your script
		#	has used. This also clears the pin numbering system in use.
		GPIO.cleanup()
