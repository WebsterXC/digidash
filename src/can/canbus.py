# File contains methods required to interact with a vehicle's CAN bus.
# This implementation uses Bluetooth V: x.xx.

class canbus(object):
    # Initialize a CAN connection with the vehicle at the given baudrate.
    def __init__(self, baudrate):
        print("__init__ not initialised")
    
    ## Method retrieves a parameter from the CAN bus via the passed pid code.
    def get(self, pid):
        print("canbus.get method not implemented")

if __name__ == "main":
    canbus.get(0x04);
