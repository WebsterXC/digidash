#################################################
#   ======    =====    ======   =====
#   ||	 \\     |     //	  |
#   ||    \\    |    // 	  |
#   ||    //    |    ||  =====	  |   --------
#   ||   //     |    \\     //	  |
#   ======    =====   ======    =====
##################################################

# [Summary]: File represents the entry point for the DigiDash unit. It starts debug logging and tries
# to establish a connection with a vehicle's CAN bus (via bluetooth). This file also starts many of
# DigiDash's background daemons and cleanup routines.

# Original Authors: #
# David Evans
# Ed Garwol
# Joe Hanson 
# Mark Grassi 
# Will Burgin

import time
import subprocess
import logging
from can import canbus, daemon, pids, automath

from DigiDash import DigiDashApp

# Initialise global logging
logpath = 'can/data/digidash.log'
log = None
def logger_init():
	logger = logging.getLogger('digilogger')
	logger.setLevel(logging.DEBUG)	

	# Remove previous log file	
	subprocess.call(['rm', logpath])

	# Set log file path, message format, and threshold to DEBUG
	fh = logging.FileHandler(logpath)
	form = logging.Formatter('%(asctime)s | %(message)s')
	fh.setLevel(logging.DEBUG)
	fh.setFormatter(form)
	logger.addHandler(fh)

	global log
	log = logger

	logger.info('Logger started.')

def exit_routine():
	log.critical('Exiting DigiDash...')
 
	# Close bluetooth socket
	try:
		print("Disconnect bluetooth")
		# Leave commented for development with no vehicle
		#canbus.BlueObject.disconnect()
	except StateError:
		log.debug("Tried to close an already closed socket.")

	# Remove previous log file	
	subprocess.call(['rm', logpath])
	# UNCOMMENT above for deployment

	# Close logging
	logging.shutdown()

def main():
	# Welcome to DigiDash! #
	
	# Initialise the global logger
	logger_init()

	#log.critical('Booting DigiDash...')

	# Check dependencies using Bash script #

	# Test to ensure a valid bluetooth connection is even possible. #
	c = canbus.canbus()		# Might need to uncomment Blue.connect() in canbus.py
		## If no, display warning and options.

	# Vehicle available.
	#d = daemon.CANDaemon()
	#d.start()

	d = daemon.ParserDaemon()
	d.start()
	#p = daemon.ParamDaemon()
	#p.start()

	#l = daemon.LoggerDaemon()
	#l.start()

	# Kivy Main Screen ("Infinite Loop for GUI")
	
	DigiDashApp().run()

	# If you got here, DigiDash exited from either an error or user-close.
	# Run exit routines.
	#exit_routine()
	
if __name__ == "__main__":
	main()
