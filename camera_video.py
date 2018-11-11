#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
S185 - Introduction to Single-Board Computers

A python script to record video to a file using the Raspberry Pi Camera Module.

Execution:
1. Set the executable flag on the script: chmod u+x camera_video.py
2. Execute with a preceding dot "./", so call ./camera_video.py

To play play the video, enter the following command:
omxplayer video.h264
or
omxplayer video.mjpeg
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
	# Set the camera resolution.
	camera.resolution = (640, 480)

	# Set the camera framerate.
	camera.framerate = 20

	# Start recording video from the camera, storing it in output.
	#	Write an H.264 video stream.
	#camera.start_recording('/home/pi/Videos/video.h264', format='h264')
	# Write an M-JPEG video stream.
	camera.start_recording('/home/pi/Videos/video.mjpeg', format='mjpeg')

	# Capture 10 seconds of video.
	camera.wait_recording(10)

	# Stop recording video from the camera.
	camera.stop_recording()

	# Stop the video preview.
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
