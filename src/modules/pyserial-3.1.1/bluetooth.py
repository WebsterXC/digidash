# File defines methods to interact with the OBDII bluetooth receiver.
# Used https://github.com/Pbartek/pyobd-pi as a guide

# The OBD-II bluetooth reader we are deploying uses ELM327 protocol to communicate.

import serial

class Bluetooth:
    isconnected = False
    available = []		# list of available bluetooth ports

    def __init__(self):

        if(0):
            print("Error, bluetooth already connected to a device.")
        else:
            print("Bluetooth object generated.")

    # Scan for available serial bluetooth connections
    def scan(identification):
        for i in range(256):
            try:
                s = serial.Serial(str(i))
                print("SERIAL")
                available.append((str(s.port)))
                s.close()
            except serial.SerialException:
                pass

        for i in range(256):
            try:
                s = serial.Serial("/dev/rfcomm"+str(i))
                print("Not rfcomm")
                available.append((str(s.port)))
                s.close()
            except serial.SerialException:
                pass

        for i in range(256):
            try:
                s = serial.Serial("/dev/ttyACM"+str(i))
                print("Not ttyACM")
                available.append((str(s.port)))
                s.close()
            except serial.SerialException:
                pass

        for i in range(256):
            try:
                s = serial.Serial("/dev/ttyUSB"+str(i))
                print("Not ttyUSB")
                
                available.append((str(s.port)))
                s.close()
            except serial.SerialException:
                pass

        for i in range(256):
            try:
                s = serial.Serial("/dev/ttyd"+str(i))
                print("Not ttyd")
                
                available.append((str(s.port)))
                s.close()
            except serial.SerialException:
                pass

    # Establish a connection with the OBDII reader.
   # def connect():
    #    numAvailable = len(available)
     #   if	numAvailable == 0:
      #      print("No Bluetooth connections available")
       # elif numAvailable == 1:
        #    # connect here
       # else:
            # let user choose which bluetooth device to connect to
            # for i in available:
                #

    # Send a list of bytes to the OBDII reader via bluetooth.
    def send(data):
        print("Bluetooth.send_bytes method not implemented")


    # Break a connection with the OBDII reader.
    def disconnect(identification):
        # isconnected = False
        # <serial connection>.close()
        print("Bluetooth.disconnect method not implemented")

x = Bluetooth()
x.scan()
