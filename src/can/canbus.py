# File contains methods required to interact with a vehicle's CAN bus.
# This implementation uses Bluetooth V: x.xx.

CANData = { }

class Canbus(object):
    # Initialize a CAN connection with the vehicle at the given baudrate.
    def __init__(self, baudrate):
        for i in range(0, 101):         # 0x00 to 0x64 
            CANData[i] = -1

        print("__init__ not initialised")
    
    ## Method retrieves a parameter from the CAN bus via the passed pid code.
    def get(self, pid):
        print("canbus.get method not implemented")

if __name__ == "main":
    canbus.get(0x04);
