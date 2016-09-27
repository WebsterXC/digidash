# File defines methods to interact with the OBDII bluetooth receiver.
# Used https://github.com/Pbartek/pyobd-pi as a guide

# The OBD-II bluetooth reader we are deploying uses ELM327 protocol to communicate.

import serial

class Bluetooth{
    isconnected = False
	available = []		# list of available bluetooth ports
	
	def scan():
		for i in range(10):
			try:
				s = serial.Serial("/dev/rfcomm"+str(i))
				available.append((str(s.port)))
				s.close()
			except serial.SerialException:
				pass
	
	def connect()
		numAvailable = len(available)
		if	numAvailable == 0:
			print("No Bluetooth connections available")	
		elif numAvailable == 1:
			# connect here
		else:
			# let user choose which bluetooth device to connect to
			# for i in available:
				#
	
    def __init__(self):

        if(isconnected):
            print("Error, bluetooth already connected to a device.")
        else:
            print("Bluetooth object generated.")

    # Send a list of bytes to the OBDII reader via bluetooth.
    def send(data):
        print("Bluetooth.send_bytes method not implemented")

    # Establish a connection with the OBDII reader.
    def connect(identification):
        isconnected = True
        print("Bluetooth.connect method not implemented")

    # Break a connection with the OBDII reader.
    def disconnect(identification):
        isconnected = False
        print("Bluetooth.disconnect method not implemented")
