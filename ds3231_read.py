#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
S185 - Introduction to Single-Board Computers

A python script that reads the DS3231 clock and calendar registers.

Execution:
1. Set the executable flag on the script: chmod u+x ds3231_read.py
2. Execute with a preceding dot "./", so call ./ds3231_read.py
"""

# Import required modules.
import sys
import time
import math
import datetime
import smbus

# Specify the I2C bus number to use.
# 	0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
try:
	bus = smbus.SMBus( 1 )
except:
	print( "ERROR: No I2C interface available." )
	sys.exit(1)

# Define the I2C address of the device.
DEVICE_ADDRESS = 0x68

# From the DS3231 datasheet (Table 1, Timekeeping Registers) these are the
# resisters that contain the clock and calendar data.
#	Register Address = 0x00	: Seconds	: 00-59
#	Register Address = 0x01	: Minutes	: 00-59
#	Register Address = 0x02	: Hours		: 00-23
#	Register Address = 0x03	: Day		: 01-07
#	Register Address = 0x04	: Date		: 01-31
#	Register Address = 0x05	: Month		: 01–12
#	Register Address = 0x06	: Year		: 00-99
ds3231_timekeeper_registers = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06]

# Lookup table for names of days.
days = ( "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday" )

# Lookup table for names of months.
months = ( 'January', 'February', 'March', 'April', 'May', 'June',
			  'July', 'August', 'September', 'October', 'November', 'December' )

# A dictionary for the Timekeeping Registers.
registers_dictionary =	{ 0x00: "Seconds",
                          0x01: "Minutes",
                          0x02: "Hours",
                          0x03: "Day",
                          0x04: "Date",
                          0x05: "Month",
                          0x06: "Year" }

# Function to convert a BCD value to an integer.
def bcd2int( value ):
	"""
	Decode a 2x4bit BCD to an integer.
	"""
	out = 0
	for d in ( value >> 4, value ):
		for p in ( 1, 2, 4 ,8 ):
			if d & 1:
				out += p
			d >>= 1
		out *= 10
	return int( out/10 )
	#return (value or 0) - 6 * ((value or 0) >> 4)


# Function to convert an integer to BCD value.
def int2bcd( value ):
	"""
	Encode a one or two integer digits number to the BCD.
	"""
	bcd = 0
	for i in (value // 10, value % 10):
		for p in (8, 4, 2, 1):
			if i >= p:
				bcd += 1
				i -= p
			bcd <<= 1
	return bcd >> 1
	#return (value or 0) + 6 * ((value or 0) // 10)

# Function to read a byte from a register address.
def readREG_byte( addr):
	"""
	Read a byte from a single register at the specified device address.
	"""
	return bus.read_byte_data( DEVICE_ADDRESS, addr )


# Function to read a block of register addresses.
def readREG_block(offset, numBytes):
	"""
	Read a block of bytes (numbytes) from address DEVICE_ADDRESS with
	an offset (offset).
	The returned value is a list of bytes.
	"""
	block = bus.read_i2c_block_data(DEVICE_ADDRESS, offset, numBytes)
	return block

# Define the main() function.
def main():
	# Display the Rapberry Pi time.
	#print("Raspberry Pi Time: ", time.ctime())

	# Read and display a block of resister values.
	offset = 0x00
	numBytes = 7
	register_block = readREG_block(offset, numBytes)
	print( "A block of {:02d} bytes from the device at address 0x{:02x}".format( numBytes, DEVICE_ADDRESS) )
	print( "with an offset of 0x{:02x}.".format( offset ) )
	print( "\t block = ", register_block )
	print( "\n" )

	#print("The date is {} {}/{}/{}".format(days[int(day)], month, date, year))
	#print("The time is {}:{:02}:{:02}".format(hours, minutes, seconds))

	# Loop over the resisters addresses and display the BCD and integer value.
	print("Device at address 0x{:02x}:".format(DEVICE_ADDRESS) )
	for address in ds3231_timekeeper_registers:
		data = readREG_byte( address )
		print( "Register BCD Data (0x{:02d}): {:02d} \t Integer Data: {:02d}  {} ".format( address, data, bcd2int(data), registers_dictionary[address] ))

		# TODO: Display/Print the time and calendar information in a human readable format.
		time.sleep(1) # wait a second
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
		# Raised when the user interrupts program execution, usually by
		# pressing Ctrl+c.
		pass
	finally:
		# No matter what has happened previously, or whether an exception was
		# thrown, execute this code as the program ends.
		# ~~~~~
		pass
