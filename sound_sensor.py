#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
S185 - Introduction to Single-Board Computers

A Python GPIO interface script that will read the input of the sound sensor
through an Analog to Digital Converter (ADC) and print it to the display.
    Derived heavily from http://kookye.com/?p=4546

Execution:
1. Set the executable flag on the script: chmod u+x sound_sensor.py
2. Execute with a preceding dot "./", so call ./sound_sensor.py
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
# Broadcom SOC.
#GPIO.setmode(GPIO.BCM)
# - or -
# Refer to the GPIO pins by the BOARD numbering system.
# This refers to the pin numbers on the P1 header of
# the Raspberry Pi board.
GPIO.setmode(GPIO.BOARD)

# Define the channel(s) that wil be used.  These are the GPIO pins on
# Raspberry Pi that will be used.
#   Input: PIN 37 / GPIO26 from Sound Sensor Out
#input_channel_list  = []
#soundChannel = 26  # GPIO26 / PIN 37
#soundChannel = 6    # GPIO06 / PIN 31
soundChannel = 23    # GPIO23 / PIN 16

#  Output: PIN 19 / GPIO10 / SPI0 MOSI from ADC PIN 11 / Din
#  Output: PIN 23 / GPIO11 / SPI0 SCLK from ADC PIN 13 / CLK
#  Output: PIN 24 / GPIO8 / SPI0 CE0 from ADC PIN 10 / !CS/SHDN
#output_channel_list = []
SPIMISO = 9     # GPIO9 / SPI0 MISO / Pin 21
SPICS = 8       # GPIO8 / SPI0 CE0 / Pin 24
SPIMOSI = 10    # GPIO10 / SPI0 MOSI / Pin 19
SPICLK = 11     # GPIO11 / SPI0 SCLK / Pin 23

# Set up the GPIO Channels - INPUT
#GPIO.setup(input_channel_list, GPIO.IN)

# Set up the GPIO Channels - OUTPUT
#GPIO.setup(output_channel_list, GPIO.OUT)



def Initialize():
   # Set Input pins
   # Set GPIO26 (soundChannel) as Input & Initialize the Pull Up/Down to UP
   GPIO.setup(soundChannel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
   GPIO.setup(SPIMISO, GPIO.IN)

   # Set Output pins
   GPIO.setup(SPIMOSI, GPIO.OUT)
   GPIO.setup(SPICLK, GPIO.OUT)
   GPIO.setup(SPICS, GPIO.OUT)
#EOF: Initialize()

# Define the main() function.
def main():
    # Initialize Constants
    SLEEP_TIME = 1

    # Initialize the Raspberry Pi
    Initialize()
    time.sleep(SLEEP_TIME)

    while True:
        if (GPIO.input(soundChannel) == False):
            print("Sound Signal Active")
            time.sleep(SLEEP_TIME)

        else:
            print("Sound Signal Inactive")
            time.sleep(SLEEP_TIME)

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
