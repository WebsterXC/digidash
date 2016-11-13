# DigiDash CAN bus abstraction to facilitate easy communication and provide a place
# for CAN bus data to be stored for repeated access.

# This class relies on the bluetooth module to communicate with an ELM327 OBDII
# reader. CAN bus data is automatically gathered via the CANDaemon class in daemon.py.

import pids
import blue
import logging
import threading

# Automatically updated PID codes
PIDcodes = [pids.ENG_RPM, pids.SPEED, pids.INTAKE_PRESS, pids.INTAKE_TEMP, pids.INTAKE_MAF, pids.OIL_TEMP, pids.FUEL_RATE, pids.THROTTLE_REQ]
CANdata = { }		# Dictionary holding all vehicle parameters + readings
CANlock = None		# Write lock for CAN dictionary
ELMdata = { }		# Dictionary holding various ELM data
ELMlock = None		# Write lock for ELM data dictionary
isConnected = False	# Is a bluetooth connection to vehicle available?
BlueObject = None	# Not sure if we want to implement it this way, but I did this because it was quick and I wanted
			# to test code.

class canbus(object):
    hasFaults   = False		# Are there DTC codes that need to be processed?
    mode	= "0x01"	# Realtime gathering mode
    #BlueObject  = None
    log		= None

    # Begin Bluetooth connection, logging, and initialise with auto-update PIDs
    def __init__(self):
	self.log = logging.getLogger('digilogger')
	
	if self.log == None:
		logging.warning("Logger file not found.")
	
	global CANlock
	CANlock = threading.Lock()

	global ELMlock
	ELMlock = threading.Lock()

	global BlueObject
	BlueObject = blue.Blue()
	#BlueObject.connect()
	
	self.log.debug('CAN connection established.')

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

	# Send pid as ELM command
	global BlueObject
	result = BlueObject.send_recv(command)

	canbus.log.debug(str.join("Sent PID: ", pid))
	canbus.log.debug(str.join("Returned: ", result))

	return result

# Nonclass method for sending ELM327 or non-MODE 1 commands to the bluetooth dongle.
def send_command(mode, cmd):
	
	# Check MODE for command type. Use MODE_ELM for ELM commands
	if mode == MODE_ELM:
		global BlueObject
		result = BlueObject.send_recv(command)
		
		canbus.log.debug(str.join("Sent ELM command: ", cmd))
		canbus.log.debug(str.join("Returned: ", result))	

	else:
		command = ((canbus.mode).split('x'))[1] + ((pid).split('x'))[1]
	
		global BlueObject
		result = BlueObject.send_recv(command)

		canbus.log.debug(str.join("Sent command: ", cmd, " with mode ", mode))
		canbus.log.debug(str.join("Returned: ", result))	

	return result

# Send MODE3 to retrieve MIL and DTC codes
def send_dtc():
	global BlueObject
	canbus.log.debug("Requested DTC codes with MODE 03.")
	return BlueObject.send_recv(pids.MODE_DTC)


# If testing standalone:
#if __name__ == "main":
#	canbus.send_command(pids.MODE_ELM, pids.ENG_RPM)
#	print("CANBUS MODULE STANDALONE")
