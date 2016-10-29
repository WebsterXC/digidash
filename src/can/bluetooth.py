# File defines methods to interact with the OBDII bluetooth receiver.
# Used https://github.com/Pbartek/pyobd-pi and https://github.com/peterh/pyobd as guides

# The OBD-II bluetooth reader we are deploying uses ELM327 protocol to communicate.

import serial
import string
import time

#port = None

class Bluetooth:
	baud = 9600
	databits = 8
	par = serial.PARITY_NONE  # parity
	sb = 1  # stop bits
	to = 0.5 # 500 millisecond timeout period for read()
	ELMver = "Unknown"
	State = 1  # state SERIAL is 1 connected, 0 disconnected (connection failed)
	port = None
	delay = 0.025

	def __init__(self):
		print("Bluetooth object generated.")

	def connect(self):
		print("Attempting to connect to vehicle.")
		try:    #note: this next line opens port
   			Bluetooth.port = serial.Serial("/dev/rfcomm0", Bluetooth.baud, parity=Bluetooth.par, stopbits=Bluetooth.sb, \
					     bytesize=Bluetooth.databits, timeout=Bluetooth.to)
			buff = ""

			# Send ATZ to clear all
			self.talk_elm("atz")
			buff = self.listen_elm()
			#buff = self.listen_elm()			

			print(buff)

			# Disable echo via ATE0
			self.talk_elm("ate0")
			buff = self.listen_elm()	

			print(buff)
	
		except serial.SerialException as e:
    			print e
    			State = 0
    			print ("Damn! Couldn't open the connection.")

		return

	def talk_elm(self, cmd):
		if Bluetooth.port != None:
			Bluetooth.port.flushOutput()
			Bluetooth.port.flushInput()
			for c in cmd:
				Bluetooth.port.write(c)
			Bluetooth.port.write("\r\n")
		else:
			print("Unable to send")
			print(cmd)
		
		time.sleep(Bluetooth.delay)

	def listen_elm(self):
		buffer = ""
		if Bluetooth.port != None:
			while 1:
				c = Bluetooth.port.read(1)
				if c == '\r' and len(buffer) > 0:
					break
				else:
					if buffer != "" or c != ">":
						buffer = buffer + c
		else:
			print("No port available.")
	
		time.sleep(Bluetooth.delay)
		return buffer
