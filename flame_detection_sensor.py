#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
S185 - Introduction to Single-Board Computers

A Python GPIO interface script that will read the input of the flame sensor
through an Analog to Digital Converter (ADC).
    Derived heavily from http://kookye.com/?p=4569

Execution:
1. Set the executable flag on the script: chmod u+x flame_detection_sensor.py
2. Execute with a preceding dot "./", so call ./flame_detection_sensor.py
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
GPIO.setmode(GPIO.BCM)
# - or -
# Refer to the GPIO pins by the BOARD numbering system.
# This refers to the pin numbers on the P1 header of
# the Raspberry Pi board.
#GPIO.setmode(GPIO.BOARD)

# Define the channel(s) that wil be used.  These are the GPIO pins on
# Raspberry Pi that will be used.
#   Input: PIN 11 / GPIO17 / SPI CE1 from Flame Sensor Digital Out
#   Input: PIN 21 / GPIO9 / SPI0 MISO from ADC PIN 12 / Dout
#input_channel_list  = []
#  Output: PIN 19 / GPIO10 / SPI0 MOSI from ADC PIN 11 / Din
#  Output: PIN 23 / GPIO11 / SPI0 SCLK from ADC PIN 13 / CLK
#  Output: PIN 24 / GPIO8 / SPI0 CE0 from ADC PIN 10 / !CS/SHDN
#output_channel_list = []
DO_pin = 17     # PIN 11 / GPIO 17 / SPI1 CE1 from output of Flame Digital Output
AO_pin = 0      # Channel 0 on the ADC

# SPI pins
SPIMISO = 9     # GPIO9 / SPI0 MISO / Pin 21
SPICS = 8       # GPIO8 / SPI0 CE0 / Pin 24
SPIMOSI = 10    # GPIO10 / SPI0 MOSI / Pin 19
SPICLK = 11     # GPIO11 / SPI0 SCLK / Pin 23

# Set up the GPIO Channels - INPUT
#GPIO.setup(input_channel_list, GPIO.IN)

# Set up the GPIO Channels - OUTPUT
#GPIO.setup(output_channel_list, GPIO.OUT)


# Function to initialize the Raspberry Pi
def Initialize():
    # Set Input pins
    # Set GPIO17 (DO_pin) as Input & Initialize the Pull Up/Down to UP
    GPIO.setup(DO_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(SPIMISO, GPIO.IN)

    # Set Output pins
    GPIO.setup(SPIMOSI, GPIO.OUT)
    GPIO.setup(SPICLK, GPIO.OUT)
    GPIO.setup(SPICS, GPIO.OUT)
#EOF: Initialize()


# Function to read from the MCP3008 ADC
#   INPUTS:
#       adcChn = channel of the ADC to be read
#       pinCLK = ADC CLK pin (PIN 13)
#       pinDin = ADC Din pin (PIN 11)
#       pinDout = ADC Dout pin (PIN 12
#       pinCS = ADC Chip Select / Shutdown (!CS/SHDN) pin (PIN 10)
#   OUTPUTS:
#       adcOut = ADC Output
def ReadFromADC(adcChn, pinCLK, pinDin, pinDout, pinCS):
    # Check for Input ADC Channel Error / Out of Bounds
    if ((adcChn > 7) or (adcChn < 0)):
        return -1

    # Set !CS (Channel Select) Pin High to Initialize the ADC
    GPIO.output(pinCS, True)

    # Set CLK & CS Low
    GPIO.output(pinCLK, False)
    GPIO.output(pinCS, False)

    commandOut = adcChn
    commandOut |= 0x18      # start bit + single-ended bit
    commandOut <<= 3        # shift 0x18 + chn up to front of the word (remove leading 0s)

    # loop over the 5 bits to send to the ADC & set on Din
    for i in range(5):
        if (commandOut & 0x80):         # Bit is HIGH; set Din HIGH
            GPIO.output(pinDin, True)
        else:                           # Bit is LOW; set Din LOW
            GPIO.output(pinDin, False)

        # bitshift left to get the next bit
        commandOut <<= 1

        # Toggle CLK pin
        GPIO.output(pinCLK, True)
        GPIO.output(pinCLK, False)

    # Read from ADC
    # ADC outputs one empty bit, one null bit then 10 ADC bits
    adcOut = 0
    for i in range(12):
        # Toggle CLK pin to start read
        GPIO.output(pinCLK, True)
        GPIO.output(pinCLK, False)
        adcOut <<= 1

        # Check if Dout is High & add a 1 to adcOut
        if (GPIO.input(pinDout)):
            adcOut |= 0x1

    # Clear the !CS bit to end the read cycle
    GPIO.output(pinCS, True)

    adcOut >>= 1    # drop the LSB in adcOut since we shifted an extra bit above

    return adcOut
#EOF: ReadFromADC()


# Define the main() function.
def main():
    # Initialize Constants
    SLEEP_TIME = 1

    # Initialize the Raspberry Pi
    Initialize()
    time.sleep(2)   # Sleep for 2 seconds
    print("Detecting Flame...")

    while True:
        flameValue = ReadFromADC(AO_pin, SPICLK, SPIMOSI, SPIMISO, SPICS)

        #DEBUG: Print ADC Value constantly
        print("ADC Value = %.1f V" % ((1024-flameValue)/1024. * 3.3))


        # Check the Flame Sensor Digital Output Pin (Is a flame detected or not?)
        if GPIO.input(DO_pin) == False: # Flame is not detected
            print("*************")
            print("*** SAFE! ***")
            print("")
            time.sleep(SLEEP_TIME)

        else:                           # Flame is detected
            print("*************")
            print("*** FIRE! ***")
            print("Fire ADC Value = %.1f V" % ((1024-flameValue)/1024. * 3.3))
            print("*************")
            print("")
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
