#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
S185 - Introduction to Single-Board Computers

A Python GPIO interface script for the HC-SR501 Infrared PIR Motion Detector.

Execution:
1. Set the executable flag on the script: chmod u+x hcsr501_infrared_pir.py
2. Execute with a preceding dot "./", so call ./hcsr501_infrared_pir.py
"""

#  Import required modules.
import os
import sys
import argparse
import time
import datetime

# Import the RPi.GPIO module/library.  This is the package that provides a GPIO
# interface.
try:
	import RPi.GPIO as GPIO
except RuntimeError:
	print("Error importing RPi.GPIO!")

# Select the GPIO numbering scheme.
# Refer to the GPIO pins by the channel numbers on the Broadcom SOC.
#GPIO.setmode(GPIO.BCM)
# - or -
# Refer to the GPIO pins by the BOARD numbering system.
#  This refers to the pin numbers on the P1 header of the Raspberry Pi board.
GPIO.setmode(GPIO.BOARD)

# Define the channel(s) that will be used. These are the GPIO pins on
# Raspberry Pi that will be used.
# Set up the GPIO Channels - INPUT
#  Input: PIN 7 / GPIO 4
# This GPIO pin is connected to the PIR sensor.
input_channel_list  = [7]
#  Output: PIN ?? (GPIO??)
#output_channel_list = []

# Set up the GPIO Channels - INPUT
GPIO.setup(input_channel_list, GPIO.IN)
# Set up the GPIO Channels - OUTPUT
#GPIO.setup(output_channel_list, GPIO.OUT)

# Define the main() function.
def main():
	print("HC-SR501 PIR Motion Detector/Sensor")

	Current_State = 0
	Previous_State = 0

	print("Waiting for PIR to settle...")

	# Loop until the PIR sensor output pin is LOW/0/FALSE
	start_time = datetime.datetime.now()	# Taking current time as starting time.

	while GPIO.input(input_channel_list[0])==1:
		Current_State  = 0

	end_time = datetime.datetime.now()		# Taking current time as the ending time.
	elapsed_time = end_time - start_time

	# Display that the PIR sensor is ready.
	print("Device initialization completed, the PIR Sensor is ready.")
	print("Initialization Time: {0}".format(elapsed_time))


	while True :
		# Read PIR output pin state.
		Current_State = GPIO.input(input_channel_list[0])

		if Current_State==1 and Previous_State==0:
			# The PIR sensor is triggered.
			start_time=datetime.datetime.now()
			print("Motion detected!")
			# Record the current state (HIGH/1/TRUE) as the previous state.
			Previous_State=1
		elif Current_State==0 and Previous_State==1:
			# The PIR has returned to a ready state.
			stop_time=datetime.datetime.now()
			print("Ready")
			elapsed_time=stop_time-start_time
			print("Reset Time: {0}".format(elapsed_time))
			Previous_State=0

		# Loop delay, wait for 1 milliseconds. It should be less than detection delay.
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
