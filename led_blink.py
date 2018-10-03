#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
S185 - Introduction to Single-Board Computers

A simple python script that will flash a LED at a constant rate.

Execution:
1. Set the executable flag on the script: chmod u+x led_blink.py
2. Execute with a preceding dot "./", so call ./led_blink.py 
"""

# Import required modules.
import os
import sys
import argparse
import time

# Import the RPi.GPIO module/library.
import RPi.GPIO as GPIO

# Select the GPIO numbering scheme.
# Refer to the GPIO pins by the channel numbers on the
#	Broadcom SOC.
GPIO.setmode(GPIO.BCM)
# - or -
# Refer to the GPIO pins by the BOARD numbering system.
#	This refers to the pin numbers on the P1 header of 
#	the Raspberry Pi board.
#GPIO.setmode(GPIO.BOARD)

# Define the channel(s) that wil be used.  These are the GPIO pins on
# Raspberry Pi that will be used.
#   Input: PIN ?? (GPIO??)
#input_channel_list  = []
#  Output: PIN 22 (GPIO25)
output_channel_list = [25]

# Set up the GPIO Channels - INPUT
#GPIO.setup(input_channel_list, GPIO.IN)

# Set up the GPIO Channels - OUTPUT
GPIO.setup(output_channel_list, GPIO.OUT);

# Define the main() function.
def main():
	# Loop forever until the user presses Ctrl+c.
	while True:
		# Turn the LED on for 1 second.
		GPIO.output(output_channel_list[0], True);   # set to 1/GPIO.HIGH/True
		time.sleep(1);
		# Turn the LED off for 1 second.
		GPIO.output(output_channel_list[0], False);  # set to 0/GPIO.FALSE/False
		time.sleep(1);
# EOF: main()


# ------------------------------------------------- BEGIN EXECUTION HERE --
if __name__ == '__main__':
	try:
		# Invoke the main function.
		main()
	except KeyboardInterrupt:
		# Raised when the user interrupts program execution, 
		#	usually by pressing Ctrl+c.
		pass
	finally:
		print("Cleaning up...")
		# Reset the status of the GPIO pins.
      GPIO.cleanup()