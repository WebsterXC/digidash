#################################################
#   ======    =====    ======   =====
#   ||	 \\     |     //	  |
#   ||    \\    |    // 	  |
#   ||    //    |    ||  =====	  |   --------
#   ||   //     |    \\     //	  |
#   ======    =====   ======    =====
##################################################

# [Summary]: This file contains the canbus class, a bluetooth abstraction that makes
# communicating with the vehcile easier. In fact, the class itself is just an objectification
# of the bluetooth connect/disconnect commands - the rest of the methods to communicate with
# the vehicle through the ELM327 dongle are nonclass. In many cases, a developer might want
# to send data to the ELM327 dongle or vehicle without a formal canbus object.

from blue import Blue, StoppedError, NoDataError, InvalidCmdError, StateError, ConnectFailureError
import blue
import logging
import threading
import pids

# List contains PID codes that are automatically grabbed by the CANDaemon at boot.
PIDcodes = [pids.ENG_RPM, pids.SPEED, pids.INTAKE_PRESS, pids.INTAKE_TEMP, pids.INTAKE_MAF, pids.THROTTLE_REQ]
CANdata = { }		# Dictionary holding the most recent { PID, value } pinged from the vehicle.
BlueObject = None	# Bluetooth object 

class canbus(object):
    mode	= pids.MODE_REALTIME	# Realtime gathering mode
    log		= None

    # Begin Bluetooth connection, logging, and initialise PIDs in dictionary.
    def __init__(self):
	canbus.log = logging.getLogger('digilogger')
	
	if canbus.log == None:
		logging.warning("Logger file not found.")
	
	global BlueObject
	BlueObject = blue.Blue()
	
	try:
		#BlueObject.connect()
		print("Fake Connection!")
	except ConnectFailureError:
		canbus.log.error("Unable establish a CAN connection.")	
		return
	except StateError:
		canbus.log.info("Tried to reconnect with an open connection?")
		return	

	canbus.log.debug('CAN connection established.')

	# Initial value for all auto-update PIDs
	for code in PIDcodes:
		CANdata[code] = 0.00

 
# Given a valid PID code, this method returns the raw data corresponding to the reply from the
# ELM327 dongle; it should also be passed through the appropriate parameter conversion function
# (see can/automath.py).
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
		return ""
	except InvalidCmdError:
		canbus.log.info(''.join(("Sent invalid PID ", pid)) ) 
		return ""
	except StoppedError:
		canbus.log.error(''.join(("Connection STOPPED after sending: ", pid)) )
		return ""
	except NoDataError:
		canbus.log.info(''.join(("Sending PID ", pid, " return NO DATA.")) )
		return ""

	canbus.log.debug(''.join(("Sent PID: ", pid)) )
	canbus.log.debug(''.join(("Returned: ", result)) )

	return result

# Method sends other types of commands to the ELM327 dongle: they could be either ELM327 
# specific commands (like turning echoes off), or DTC commands (mode 03 gathering).
# Modes are defined in can/pids.py.
def send_command(mode, pid):
	
	# ELM commands and DTC commands are formatted differently
	if mode == pids.MODE_ELM:
		command = pid
	elif mode == pids.MODE_DTC:
		command = mode		# cmd arguement doesn't matter if mode is 0x03
	else:
		command = ((mode).split('x'))[1] + ((pid).split('x'))[1]
		

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

	time.sleep(0.1)

	return result

# Method ensures safe addition of a PID to the list of automatically updated replies from the vehicle's
# CAN bus. In addition to adding the PID to PIDcodes, an entry must be generated in the CAN global
# dictionary, so that DigiDash know this PID exists and is supported by the vehicle.
def subscribe(pid):
	if not isinstance(pid, basestring):
		return

	global PIDcodes
	if pid not in PIDcodes:
		global CANdata
		CANdata[pid] = 0.00;

		global PIDcodes
		PIDcodes.append(pid)
