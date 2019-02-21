#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
S185 - Introduction to Single-Board Computers

A Python GPIO interface script that will read the DHT11 Temperature & Humidity
Sensor Module output.  Derived heavily from http://kookye.com/?p=4539.

Execution:
1. Set the executable flag on the script: chmod u+x dht11_sensor.py
2. Execute with a preceding dot "./", so call ./dht11_sensor.py
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
#   Input: PIN ?? (GPIO??)
input_channel  = 4
#input_channel_list  = [4]
#  Output: PIN ?? (GPIO??)
#output_channel_list = []

# Set up the GPIO Channels - INPUT
#GPIO.setup(input_channel_list, GPIO.IN)

# Set up the GPIO Channels - OUTPUT
#GPIO.setup(output_channel_list, GPIO.OUT)


# Function to send a value and sleep for the input period
def SendAndSleep(channel, value, sleepTime):
    GPIO.output(channel, value)
    time.sleep(sleepTime)
#EOF: SendAndSleep()


# Function to read the data from the Data Pin of the DHT11 Sensor
def CollectInput(channel):
    # initialize the data counters
    unchanged_count = 0         # counter to collect data while it is unchanged
    max_unchanged_count = 100   # maximum count to determine the end of the data

    last = -1
    data = []
    while True:
        current = GPIO.input(channel)
        data.append(current)
        if last != current:
            unchanged_count = 0
            last = current
        else:
            unchanged_count = unchanged_count + 1
            if unchanged_count > max_unchanged_count:
                break

    return data
#EOF: CollectInput()


# Function to parse the lengths of the data pull up
def ParseDataPullUpLengths(data):
    # Define states for state machine
    STATE_INIT_PULL_DOWN        = 1
    STATE_INIT_PULL_UP          = 2
    STATE_DATA_FIRST_PULL_DOWN  = 3
    STATE_DATA_PULL_UP          = 4
    STATE_DATA_PULL_DOWN        = 5

    state = STATE_INIT_PULL_DOWN    # initial state

    lengths = []        # array to contain lengths of data pull up periods
    current_length = 0  # length of previous period

    # start state machine
    for i in range(len(data)):
        current = data[i]
        current_length = current_length + 1

        # State 1: STATE_INIT_PULL_DOWN
        if state == STATE_INIT_PULL_DOWN:
            if current == GPIO.LOW:
                # Received initial pull down, transition to next state
                state = STATE_INIT_PULL_UP
                continue
            else:
                continue

        # State 2: STATE_INIT_PULL_UP
        if state == STATE_INIT_PULL_UP:
            if current == GPIO.HIGH:
                # Received initial pull up, transition to next state
                state = STATE_DATA_FIRST_PULL_DOWN
                continue
            else:
                continue

        # State 3: STATE_DATA_FIRST_PULL_DOWN
        if state == STATE_DATA_FIRST_PULL_DOWN:
            if current == GPIO.LOW:
                # Received initial data pull down; next state will be data pull up
                state = STATE_DATA_PULL_UP
                continue
            else:
                continue

        # State 4: STATE_DATA_PULL_UP
        if state == STATE_DATA_PULL_UP:
            if current == GPIO.HIGH:
                # Received data pull up; length of this will determine 0/1
                current_length = 0
                state = STATE_DATA_PULL_DOWN
                continue
            else:
                continue

        # State 5: STATE_DATA_PULL_DOWN
        if state == STATE_DATA_PULL_DOWN:
            if current == GPIO.LOW:
                # Received data pull down; store the length of the pull up period & go back to state 4
                lengths.append(current_length)
                state = STATE_DATA_PULL_UP
                continue
            else:
                continue

    return lengths
#EOF: ParseDataPullUpLengths()


# Function to identify the bits of the data
def CalculateBits(lengths):
    # Initialize shortest & longest pull up periods
    shortest_pull_up = 1000
    longest_pull_up = 0

    # Find the shortest and longest periods
    for i in range(0, len(lengths)):
        length = lengths[i]
        if length < shortest_pull_up:
            shortest_pull_up = length

        if length > longest_pull_up:
            longest_pull_up = length

    # Find the middle to determine the threshold
    threshold = shortest_pull_up + (longest_pull_up - shortest_pull_up) / 2

    bits = []

    # Determine whether it is true or false
    for i in range(0, len(lengths)):
        bit = False
        if lengths[i] > threshold:
            bit = True

        bits.append(bit)

    return bits
#EOF: CalculateBits()


# Function to convert bits to bytes
def BitsToBytes(bits):
    bytes = []
    byte = 0

    # loop over the bits & calculate the value
    for i in range(0, len(bits)):
        byte = byte << 1
        if (bits[i]):
            byte = byte | 1
        else:
            byte = byte | 0

        if ((i + 1) % 8 == 0):
            bytes.append(byte)
            byte = 0

    return bytes
#EOF: BitsToBytes()


# Function to Calculate the Checksum
def CalculateChecksum(bytes):
    return bytes[0] + bytes[1] + bytes[2] + bytes[3] & 255
#EOF: CalculateChecksum


# Function to Convert Degrees Celcius to Fahrenheit
def C2F(degC):
    return 1.8 * degC + 32

#EOF: C2F()


# Define the main() function.
def main():
    
    # Define Error Codes
    ERR_NO_ERROR = 0
    ERR_MISSING_DATA = 1
    ERR_CRC = 2

    # Initialize the Sensor
    GPIO.setup(input_channel, GPIO.OUT)

    # Send Start Signal (HIGH then LOW for at least 18 ms)
    SendAndSleep(input_channel, GPIO.HIGH, 0.05)    # send initial HIGH for 50 ms
    SendAndSleep(input_channel, GPIO.LOW, 0.02)     # send LOW for 20 ms

    # Change Pin to Pull Up Input
    GPIO.setup(input_channel, GPIO.IN, GPIO.PUD_UP)

    # Read the Data
    data = CollectInput(input_channel)

    # Parse lenghs of the data periods (pulled-up)
    pull_up_lengths = ParseDataPullUpLengths(data)

    # Check bit count & return error if it isn't correct length
    if len(pull_up_lengths) != 40:
        print("ERROR: Error Code: %d - Bit Count Not Correct" % (ERR_MISSING_DATA))
        return

    # Calculate each bit in the data from the pull up lengths
    bits = CalculateBits(pull_up_lengths)

    # Convert the bits to bytes
    bytes = BitsToBytes(bits)

    # Calculate Checksum & check for errors
    checksum = CalculateChecksum(bytes)
    if bytes[4] != checksum:
        print("ERROR: Error Code: %d - CRC Error" % (ERR_CRC))
        return

    # If we have not errored out yet, we have valid data
    tempC = bytes[2]
    tempF = C2F(tempC)
    humidity = bytes[0]
    print("Temp = %d C\tTemp = %d F\tHumidity = %d %%" % (tempC, tempF, humidity))
    return

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
