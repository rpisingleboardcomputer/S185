#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
S185 - Introduction to Single-Board Computers

A python script to get the model of the Raspberry Pi.

Execution:
1. Set the executable flag on the script: chmod u+x rpimodel.py
2. Execute with a preceding dot "./", so call ./rpimodel.py

"""

#  Import required modules.
import subprocess
import os
import sys
import argparse
import time

# Define the main() function.
def main():
	s = os.system("cat /proc/device-tree/model")
	print(s)
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
		# Executed before leaving the try statement, whether an exception
		#	has occurred or not.
		pass
