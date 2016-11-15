# DigiDash CAN bus abstraction to facilitate easy communication and provide a place
# for CAN bus data to be stored for repeated access.

# This class relies on the bluetooth module to communicate with an ELM327 OBDII
# reader. CAN bus data is automatically gathered via the CANDaemon class in daemon.py.

import pids
from blue import Blue, StoppedError, NoDataError, InvalidCmdError, StateError, ConnectFailureError
import blue
import logging
import threading

# Automatically updated PID codes
PIDcodes = [pids.ENG_RPM, pids.SPEED, pids.INTAKE_PRESS, pids.INTAKE_TEMP, pids.INTAKE_MAF, pids.FUEL_RATE, pids.ENG_TORQUE_ACT, pids.THROTTLE_REQ]
CANdata = { }		# Dictionary holding all vehicle parameters + readings
CANlock = None		# Write lock for CAN dictionary
ELMdata = { }		# Dictionary holding various ELM data
ELMlock = None		# Write lock for ELM data dictionary
isConnected = False	# Is a bluetooth connection to vehicle available?
BlueObject = None	# Not sure if we want to implement it this way, but I did this because it was quick and I wanted
			# to test code.

class canbus(object):
    hasFaults   = False			# Are there DTC codes that need to be processed?
    mode	= pids.MODE_REALTIME	# Realtime gathering mode
    log		= None

    # Begin Bluetooth connection, logging, and initialise with auto-update PIDs
    def __init__(self):
	canbus.log = logging.getLogger('digilogger')
	
	if canbus.log == None:
		logging.warning("Logger file not found.")
	
	global CANlock
	CANlock = threading.Lock()

	global ELMlock
	ELMlock = threading.Lock()

	global BlueObject
	BlueObject = blue.Blue()
	
	try:
		print("Fake connection!")
		#BlueObject.connect()
	except ConnectFailureError:
		canbus.log.error("Unable establish a CAN connection.")	
		return

	canbus.log.debug('CAN connection established.')

	# Initial value for all auto-update codes
	for code in PIDcodes:
		CANdata[code] = 0.00
    
# Method retrieves a parameter from the CAN bus via the passed pid code.
def send_pid(pid):

	# If PID is not in hex format or not a string
	if isinstance(pid, (int, long) ) or "0x" not in pid:
		print(" PID must be a hexidecimal string.")
		return

	# Process and reformat PID code, then send it.
	command = ((canbus.mode).split('x'))[1] + ((pid).split('x'))[1]

	try:
		global BlueObject
		result = BlueObject.send_recv(command)
	except StateError:
		canbus.log.error(''.join(("Tried to send ", pid, " with no Bluetooth connection.")) )
		return
	except InvalidCmdError:
		canbus.log.info(''.join(("Sent invalid PID ", pid)) ) 
		return
	except StoppedError:
		canbus.log.error(''.join(("Connection STOPPED after sending: ", pid)) )
		return
	except NoDataError:
		canbus.log.info(''.join(("Sending PID ", pid, " return NO DATA.")) )
		return

	canbus.log.debug(''.join(("Sent PID: ", pid)) )
	canbus.log.debug(''.join(("Returned: ", result)) )

	return result

# Nonclass method for sending ELM327 or non-MODE 1 commands to the bluetooth dongle.
def send_command(mode, cmd):
	
	# ELM commands and DTC commands are formatted differently
	if mode == MODE_ELM:
		command = cmd
	elif mode == MODE_DTC:
		command = mode		# cmd arguement doesn't matter if mode is 0x03
	else:
		command = ((canbus.mode).split('x'))[1] + ((pid).split('x'))[1]
		

	# Send / Receive the result
	try:
		result = BlueObject.send_recv(command)
	except StateError:
		canbus.log.error(''.join(("Tried to send ", pid, " with no Bluetooth connection.")) )
		return
	except InvalidCmdError:
		canbus.log.info(''.join(("Sent invalid PID ", pid)) ) 
		return
	except StoppedError:
		canbus.log.error(''.join(("Connection STOPPED after sending: ", pid)) )
		return
	except NoDataError:
		canbus.log.info(''.join(("Sending PID ", pid, " return NO DATA.")) )
		return
	
	canbus.log.debug(''.join(("Sent command: ", command, " in mode ", mode)) )
	canbus.log.debug(''.join(("Returned: ", result)) )

	return result

# Glorified list append for auto-update PIDs.
def subscribe(pid):
	if not isinstance(pid, basestring):
		return

	global PIDcodes
	if pid not in PIDcodes:
		global PIDcodes
		PIDcodes.append(pid)
	else:
		global PIDcodes
		PIDcodes.pop(PIDcodes.index(pid))


# If testing standalone:
#if __name__ == "main":
#	canbus.send_command(pids.MODE_ELM, pids.ENG_RPM)
#	print("CANBUS MODULE STANDALONE")
