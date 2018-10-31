
#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
S185 - Introduction to Single-Board Computers

A python script to capture an image and preview it using the
Raspberry Pi Camera Module.

Execution:
1. Set the executable flag on the script: chmod u+x camera_preview.py
2. Execute with a preceding dot "./", so call ./camera_preview.py
"""

#  Import required modules.
import os
import sys
import argparse
import time

# Import the Picamera module.
try:
	import picamera
except RuntimeError:
	print("Error importing Picamera module!")

# Create an instance of the Picamera class.
camera = picamera.PiCamera()

# Define the main() function.
def main():
	# Displays the preview overlay.
	camera.start_preview()
	# Displays the preview overlay for 10 seconds.
	time.sleep(10)
	# Closes the preview overlay.
	camera.stop_preview()
# EOF: main()


# ------------------------------------------------- BEGIN EXECUTION HERE --
if __name__ == '__main__':
	try:
		# Invoke the main function.
		main()
	except KeyboardInterrupt:
		# Raised when the user interrupts program execution, usually by pressing
		#  Ctrl+c.
		pass
	finally:
		# No matter what has happened previously, or whether an
		# exception was thrown, execute this code as the program ends.
		# ~~~~~
		print("Cleaning up...")
		# Finalizes the state of the camera.
		# This method stops all recording and preview activities and releases
		#	all resources associated with the camera; this is necessary to
		#	prevent GPU memory leaks.
      camera.close()
