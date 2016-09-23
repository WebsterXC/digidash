# File defines methods to iteract with the OBDII bluetooth receiver.

class Bluetooh{
    isconnected = False

    def __init__(self):
        if(isconnected):
            print("Error, bluetooth already connected to a device.")
        else:
            print("Bluetooth object generated.")

    # Send a list of bytes to the OBDII reader via bluetooth.
    def send_bytes(data):
        print("Bluetooth.send_bytes method not implemented")

    # Establish a connection with the OBDII reader.
    def connect(identification):
        isconnected = True
        print("Bluetooth.connect method not implemented")

    # Break a connection with the OBDII reader.
    def disconnect(identification):
        isconnected = False
        print("Bluetooth.disconnect method not implemented")
