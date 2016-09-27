# File defines methods to interact with the OBDII bluetooth receiver.
# Used https://github.com/Pbartek/pyobd-pi as a guide

import serial

class Bluetooth:
    isconnected = False
    available = []		# list of available bluetooth ports

    def __init__(self):
        if(isconnected):
            print("Error, bluetooth already connected to a device.")
        else:
            print("Bluetooth object generated.")

    # Scan for available serial bluetooth connections
    def scan(identification):
        for i in range(10):
            try:
                s = serial.Serial("/dev/rfcomm"+str(i))
                available.append((str(s.port)))
                s.close()
            except serial.SerialException:
                pass


    # Establish a connection with the OBDII reader.
	def connect():
        numAvailable = len(available)
        if	numAvailable == 0:
            print("No Bluetooth connections available")
        elif numAvailable == 1:
            # connect here
        else:
            # let user choose which bluetooth device to connect to
            # for i in available:
                #

    # Send a list of bytes to the OBDII reader via bluetooth.
    def send_bytes(data):
        print("Bluetooth.send_bytes method not implemented")


    # Break a connection with the OBDII reader.
    def disconnect(identification):
        isconnected = False
        # <serial connection>.close()
        print("Bluetooth.disconnect method not implemented")
