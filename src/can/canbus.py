# DigiDash CAN bus abstraction to facilitate easy communication and provide a place
# for CAN bus data to be stored for repeated access.

# This class relies on the bluetooth module to communicate with an ELM327 OBDII
# reader. CAN bus data is automatically gathered via the CANDaemon class in daemon.py.

import pids
#import bluetooth

CANdata = { }		# Dictionary holding all vehicle parameters + readings
PIDcodes = [ ]		# Vehicle parameters automatically updated above

class canbus(object):
    isConnected = False		# Is a bluetooth connection to vehicle available?
    hasFaults   = False		# Are there DTC codes that need to be processed?
    mode	= "0x01"	# Realtime gathering mode

    # Initialize a CAN connection with the vehicle at the given baudrate.
    def __init__(self):
        print("__init__ not initialised")

    
# Method retrieves a parameter from the CAN bus via the passed pid code.
def send_pid(pid):

	# If PID is not in hex format or not a string
	if isinstance(pid, (int, long) ) or "0x" not in pid:
		print(" PID must be a hexidecimal string.")
		return

	# Process and reformat PID code
	command = ((canbus.mode).split('x'))[1] + ((pid).split('x'))[1]

	# Send command via ELM327

	# Gather response and return answer
	return 0

# Sends an ELM327 specific command to the bluetooth receiver.
# "Static" method for sending ELM327 commands since the canbus object may
# not be ready yet.
def send_command(cmd):
	
	# If it's clearly not an ELM command



# If testing standalone:
if __name__ == "main":
    send_pid(ENG_RPM)
