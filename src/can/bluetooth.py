# File defines methods to iteract with the OBDII bluetooth receiver.

# The OBD-II bluetooth reader we are deploying uses ELM327 protocol to communicate.

import serial

class Bluetooh{
    baudrate = 9600
    isconnected = False

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
