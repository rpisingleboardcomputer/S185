#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
S185 - Introduction to Single-Board Computers

A python script that drives an LED with an 4N35 Optocoupler.

#Execution:
#1. Set the executable flag on the script: chmod u+x 4n35.py
#2. Execute with a preceding dot "./", so call ./4n35.py
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
#GPIO.setmode(GPIO.BCM)
# - or -
# Refer to the GPIO pins by the BOARD numbering system.
#  This refers to the pin numbers on the P1 header of the Raspberry Pi board.
GPIO.setmode(GPIO.BOARD)

# Define the channel(s) that will be used.  These are the GPIO pins on
# Raspberry Pi that will be used.
#   Input: PIN ?? (GPIO??)
#input_channel = ?
#input_channel_list = [?]
#  Output: PIN 22 (GPIO25)
output_channel = 22
#output_channel_list = [?]

# Set up the GPIO Channels - INPUT
#GPIO.setup(input_channel, GPIO.IN)
#GPIO.setup(input_channel_list, GPIO.IN)

# Set up the GPIO Channels - OUTPUT
#  Set the initial level to HIGH (3.3v)
GPIO.setup(output_channel, GPIO.OUT, initial=GPIO.HIGH)
#GPIO.setup(output_channel_list, GPIO.OUT)

# Define the main() function.
def main():
	# loop forever until user presses Ctrl+c
	while True:
		# Turn the LED off.
		#print("<<<DEBUG>>> Turning LED Off.")
		GPIO.output(output_channel, GPIO.LOW)	# set PIN 22 (GPIO25) to 0/GPIO.LOW/False
		time.sleep(0.3)
		# Turn the LED on.
		#print("<<<DEBUG>>> \tTurning LED On.")
		GPIO.output(output_channel, GPIO.HIGH)	# set PIN 22 (GPIO25) to 1/GPIO.HIGH/True
		time.sleep(0.3)
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

