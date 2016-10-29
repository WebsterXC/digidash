# DigiDash CAN bus abstraction to facilitate easy communication and provide a place
# for CAN bus data to be stored for repeated access.

# This class relies on the bluetooth module to communicate with an ELM327 OBDII
# reader. CAN bus data is automatically gathered via the CANDaemon class in daemon.py.

import pids
import bluetooth

# Automatically updated PID codes
PIDcodes = [pids.ENG_RPM, pids.SPEED, pids.INTAKE_PRESS, pids.INTAKE_TEMP, pids.INTAKE_MAF, pids.OIL_TEMP, pids.FUEL_RATE, pids.THROTTLE_REQ]
CANdata = { }		# Dictionary holding all vehicle parameters + readings
isConnected = False	# Is a bluetooth connection to vehicle available?
BlueObject = None	# Not sure if we want to implement it this way, but I did this because it was quick and I wanted
			# to test code.

class canbus(object):
    hasFaults   = False		# Are there DTC codes that need to be processed?
    mode	= "0x01"	# Realtime gathering mode
    #BlueObject  = None

    # Begin Bluetooth connection and initialise with auto-update PIDs
    def __init__(self):
	global BlueObject
	BlueObject = bluetooth.Bluetooth()
	BlueObject.connect()

	for code in PIDcodes:
		CANdata[code] = 0.00
    
# Method retrieves a parameter from the CAN bus via the passed pid code.
def send_pid(pid):

	# If PID is not in hex format or not a string
	if isinstance(pid, (int, long) ) or "0x" not in pid:
		print(" PID must be a hexidecimal string.")
		return

	# Process and reformat PID code
	command = ((canbus.mode).split('x'))[1] + ((pid).split('x'))[1]

	global BlueObject
	# Send command via ELM327
	BlueObject.talk_elm(command)	

	# Gather response and return answer
	result = BlueObject.listen_elm()

	return result

# Nonclass method for sending ELM327 commands to the bluetooth dongle, since the canbus object may not be ready yet.
def send_command(cmd):
	print("Unimplemented")
	return isConnected


# If testing standalone:
#if __name__ == "main":
	#send_pid(ENG_RPM)
#	print("CANBUS MODULE STANDALONE")
