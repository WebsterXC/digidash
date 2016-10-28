# File defines methods to interact with the OBDII bluetooth receiver.
# Used https://github.com/Pbartek/pyobd-pi and https://github.com/peterh/pyobd as guides

# The OBD-II bluetooth reader we are deploying uses ELM327 protocol to communicate.

import serial
import string
import time

class Bluetooth:
	baud = 9600
	databits = 8
	par = serial.PARITY_NONE  # parity
	sb = 1  # stop bits
	to = 0.5 # 500 millisecond timeout period for read()
	ELMver = "Unknown"
	State = 1  # state SERIAL is 1 connected, 0 disconnected (connection failed)
	port = None
	delay = 0.05

	def __init__(self):
		print("Bluetooth object generated.")

	def connect(self):
		print("Attempting to connect to vehicle.")
		try:    #note: this next line opens port
   			port = serial.Serial("/dev/rfcomm0", Bluetooth.baud, parity=Bluetooth.par, stopbits=Bluetooth.sb, \
					     bytesize=Bluetooth.databits, timeout=Bluetooth.to)

			buff = ""
	
			time.sleep(0.1)

			# Send ATZ to clear all
			talk_elm(self, "atz")
			buff = listen_elm(self)
			#listen_elm(self)			

			print(buff)

			# Disable echo via ATE0
			talk_elm(self, "ate0")
			buff = listen_elm(self)	

			print(buff)

		except serial.SerialException as e:
    			print e
    			State = 0
    			print ("Damn! Couldn't open the connection.")

		return

	def talk_elm(self, cmd):
		if port != None:
			port.flushOutput()
			port.flushInput()
			for c in cmd:
				port.write(c)
			port.write("\r\n")
		else:
			print("Unable to send")
			print(cmd)
		
		time.sleep(Bluetooth.delay)

	def listen_elm(self):
		buffer = ""
		if port != None:
			while 1:
				c = port.read(1)
				if c == '\r' and len(buffer) > 0:
					break
				else:
					if buffer != "" or c != ">":
						buffer = buffer + c
		else:
			print("No port available.")
			print(cmd)
	
		time.sleep(Bluetooth.delay)
		return buffer
