#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
S185 - Introduction to Single-Board Computers

A simple MQTT message publisher python script.

- A message has a topic and a payload, like the subject and the content of
  an email.
- The Publisher sends a message to the network.
- The Subscriber listens for messages with a particular topic.
- The Broker is responsible for coordinating the communication between
  publishers and subscribers. It can also store messages while subscribers
  are off-line.

Execution:
1. Set the executable flag on the script: chmod u+x mqtt_publisher.py
2. Execute with a preceding dot "./", so call ./mqtt_publisher.py

The subscriber to the message is done with the mosquitto subscriber.
The Mosquitto message broker/server that implements the MQTT protocol needs
to be installed on the Raspberry Pi:
   pi@raspberrypi:~ $ sudo apt-get install mosquitto mosquitto-clients
the mosquitto_sub is a simple MQTT client that will subscribe to a topic and
print the messages that it receives.

For this code, on the Raspberry Pi, open a terminal or establish a SSH
connection.  Start a subscriber in the channel "RPi_Channel" this is waiting
for a message(s) for a publisher:
   pi@raspberrypi:~ $ mosquitto_sub -d -h localhost -v -t RPi_Channel
"""

# Import required modules.
import os
import sys
import argparse
import time

# Import the MQTT module/library.  This is the package that provides a client
#  class which enable applications to connect to an MQTT broker to publish
#  messages, and to subscribe to topics and receive published messages.
try:
	import paho.mqtt.client as mqtt
except RuntimeError:
	print("Error importing the MQTT module/library!")

# Define the MQTT and Mosquitto variables.
MQTT_BROKER             = "localhost"
MQTT_PORT               = 1883
MQTT_KEEPALIVE_INTERVAL = 60
MQTT_TOPIC              = "RPi_Channel"

# Define the main() function.
def main():
	# Create an instance of the MQTT Client class.
	client = mqtt.Client()
	# Establish a connection to the Mosquitto Broker/Server.
	client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
	# Publish a message.
	client.publish(MQTT_TOPIC, "Hello Raspberry Pi!");
	# Disconnect from the Mosquitto Broker/Server.
	client.disconnect();
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
		pass
