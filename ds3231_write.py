#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
A python script that writes the time and calendar to the DS3231 registers.

Execution:
1. Set the executable flag on the script: chmod u+x ds3231_write.py
2. Execute with a preceding dot "./", so call ./ds3231_write.py
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

# Define the DS3231 register addresses for
REGISTER_ADDRESS_SECONDS 	= 0x00
REGISTER_ADDRESS_MINUTES	= 0x01
REGISTER_ADDRESS_HOURS 		= 0x02
REGISTER_ADDRESS_DAY 		= 0x03
REGISTER_ADDRESS_DATE 		= 0x04
REGISTER_ADDRESS_MONTH 		= 0x05
REGISTER_ADDRESS_YEAR 		= 0x06
REGISTER_ADDRESS_CONTROL 	= 0x07

# Lookup table for names of days.
days = ( "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday" )


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

# Function to write ...
def writeRegister_byte(register, data):
	"""
	Write a byte to a single register at the specified device address.
	"""
	bus.write_byte_data(DEVICE_ADDRESS, register, data)


# Function to set the RTC time and calendar values.
def setRTC(seconds = None, minutes = None, hours = None, day = None, date = None, month = None, year = None):
	"""
	Set the time and calendar values for the RTC module.
	"""
	if seconds is not None:
		if seconds < 0 or seconds > 59:
			 raise ValueError( 'Seconds is out of range [0,59].' )
		writeRegister_byte( REGISTER_ADDRESS_SECONDS, int2bcd(seconds) )

	if minutes is not None:
		if minutes < 0 or minutes > 59:
			 raise ValueError( 'Minutes is out of range [0,59].' )
		writeRegister_byte( REGISTER_ADDRESS_MINUTES, int2bcd(minutes) )

	if hours is not None:
		if hours < 0 or hours > 23:
			 raise ValueError( 'Hours is out of range [0,23].' )
		writeRegister_byte( REGISTER_ADDRESS_HOURS, int2bcd(hours) )

	if day is not None:
		if day < 1 or day > 7:
			 raise ValueError( 'Day of Week is out of range [1,7].' )
		writeRegister_byte( REGISTER_ADDRESS_DAY, int2bcd(day) )

	if date is not None:
		if date < 1 or day > 31:
			 raise ValueError( 'Date is out of range [1,31].' )
		writeRegister_byte( REGISTER_ADDRESS_DATE, int2bcd(date) )

	if month is not None:
		if month < 1 or month > 12:
			 raise ValueError( 'Month is out of range [1,12].' )
		writeRegister_byte( REGISTER_ADDRESS_MONTH, int2bcd(month) )

	if year is not None:
		if year < 0 or year > 99:
			 raise ValueError( 'Years is out of range [0,99].' )
		writeRegister_byte( REGISTER_ADDRESS_YEAR, int2bcd(year) )


# Define the main() function.
def main():
	# TODO:	Get the time and date from the RPi and set the RTC to those values.
	# http://robsraspberrypi.blogspot.com/2016/02/raspberry-pi-all-things-date-and-time.html
	seconds	= 0
	minutes	= 1
	hours	= 20
	day	= 2
	date	= 15
	month	= 1
	year	= 19
	print("The date is {} {}/{}/{}".format(days[int(day)], month, date, year))
	print("The time is {}:{:02}:{:02}".format(hours, minutes, seconds))
	print( "Setting the RTC time and calendar values." )
	print( " Seconds = ", seconds)
	print( " Minutes = ", minutes)
	print( " Hours   = ", hours)
	print( " Day     = ", day)
	print( " Date    = ", date)
	print( " Month   = ", month)
	print( " Year    = ", year)
	setRTC(seconds, minutes, hours, day, date, month, year)
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
