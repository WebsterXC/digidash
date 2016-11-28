# DigiDash: A plug-and-play digital dashboard and engine monitor. #

# Entry point for DigiDash digital dashboard unit. #

# This is a class project for our software engineering class, CSE442 at University at Buffalo. The
# code is provided as open-source under the GNU GPL V3 license, which can be found in the top level
# directory. If you found our code useful, please give credit in your comments!

# Authors:
# David Evans
# Ed Garwol
# Joe Hanson
# Mark Grassi
# Will Burgin
# Khan

import time
import subprocess
import logging
from can import canbus, daemon, pids, automath

#from DigiDash import DigiDashApp

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
	# Kivy (Ver: )
	# Kivy Dependency List:
	#
	#


	## KIVY START MENU HERE ##
    	

	##########################

	# Test to ensure a valid bluetooth connection is even possible. #
	c = canbus.canbus()		# Might need to uncomment Blue.connect() in canbus.py
		## If no, display warning and options.

	# Vehicle available.
	#d = daemon.CANDaemon()
	#d.start()

	#d = daemon.ParserDaemon()
	#d.start()
	#p = daemon.ParamDaemon()
	#p.start()

	#l = daemon.LoggerDaemon()
	#l.start()

	# Kivy Main Screen ("Infinite Loop for GUI")
	
	#DigiDashApp().run()

	#print(canbus.CANdata)

	while 1:
		data = []
		for pid in canbus.PIDcodes:
			data.append(automath.convert(pid, canbus.send_pid(pid)) )
	
		print(data)
		time.sleep(0.001)

	# If you got here, DigiDash exited from either an error or user-close.
	# Run exit routines.
	#exit_routine()
	

if __name__ == "__main__":
	main()
