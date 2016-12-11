#################################################
#   ======    =====    ======   =====
#   ||	 \\     |     //	  |
#   ||    \\    |    // 	  |
#   ||    //    |    ||  =====	  |   --------
#   ||   //     |    \\     //	  |
#   ======    =====   ======    =====
##################################################

# [Summary]: DigiDash uses background daemons to handle many of the complex and confusing data gathering tasks.
# This allows the program to grab information from the user's vehicle while still offering a functional and
# responsive GUI. Different daemon classes are built from Python's multithreading module, each doing a specific
# task. The thread that starts the DigiDash GUI and runs the corresponding display is considered the master thread;
# this allows proper freeing of resources when DigiDash exits.

# Background daemons and coordinate data gathering/computation in various ways.
import time
import threading
import csv
import canbus, pids
import automath
import logging

csv_file = 'can/data/data.txt'                                  # Sample data file to open
inparams = ["0x1F", "0x0C", "0x0D", "0x0F", "0x0B", "0x10", "0x11", "0x5D"] # Columns in sample data CSV

# Parser daemon reads recorded data from a CSV file and places it in the CANdata dictionary. 
# It ensures data is in the structure at the time listed in the CSV file by calculating the time
# difference and sleeping for that difference. This daemon can be used to simulate input data into
# the CANdata dictionary when a vehicle is not readily available.
class ParserDaemon(threading.Thread):
    log = None
    def __init__(self):
        threading.Thread.__init__(self)
	self.setDaemon(True)
	self.log = logging.getLogger('digilogger')

    def run(self):
	self.log.debug('ParserDaemon started.')            
 
        # Begin reading data
        parser_process()

	self.log.debug('ParserDaemon exited.')            

    # Return a piece of data given a PID code
    def get_data(self, dat):
        return canbus.CANdata.get(dat)

def parser_process():
        # 100 readthroughs of data file as a max timeout
        for i in range(0, 100):
            with open(csv_file, 'rb') as csvf:  # Open the file
                # csv_reader is an iterator and only contains 1 line at a time
                csv_reader = csv.reader(csvf, delimiter=",", quotechar="|")
            
                # Read the first line for data
                data_row = csv_reader.next()

                # Read the second line for time reference
                time_row = csv_reader.next()
		
		linenum = 0
                # While time_row is not an empty list
                while time_row:
                    
                    # Place data from row in CAN dictionary
                    counter = 0
                    for param in data_row:
			canbus.CANdata[inparams[counter]] = float(param)
			counter += 1
			
                    # Establish time quantum and wait
                    #time_now = float(data_row[0])
                    #time_later = float(time_row[0])
                    #time.sleep(time_later - time_now)

		    # Override RTES quantum with static delay for CS Ed Week Demo
		    time.sleep(0.075)

                    # Iterative housekeeping
                    data_row = time_row
		    if linenum < 1130:
			time_row = csv_reader.next()
			linenum += 1
		    else:
			csvf.seek(0)
			linenum = 0

# The CANDaemon handles the automated parameter gathering ability of DigiDash. Referencing the PIDcodes
# list in canbus.py, the daemon cyclically asks the vehicle for those PIDs and automatically updates
# the CANdata dictionary. What results is that the CANdata dictionary always has the most recent possible
# parameter value for each of the PIDs in canbus.PIDcodes. When a gauge is added to the screen, it's PID
# is added to the list that CANdaemon reads from, allowing for seamless gauge configuration. It is safe 
# to use canbus.send_pid and canbus.send_command while this daemon is running.
class CANDaemon(threading.Thread):
    log = None
    def __init__(self):
        threading.Thread.__init__(self)
	self.setDaemon(True)
	self.log = logging.getLogger('digilogger')		

    def run(self):
        # Begin reading data
	self.log.debug("CANDaemon started")
        can_process()
	self.log.debug("CANDaemon exited.")

def can_process():
	while 1:
		# Iterate through PIDcodes and get data for each. Place in CANdata.
		for pid in canbus.PIDcodes:
			answer = canbus.send_pid(pid)

			if answer == None or answer == "":
				continue

			canbus.CANdata[pid] = automath.convert(pid, answer)

# This daemon gathers engine data for a specified period of time and then writes it to a CSV file.
# WARNING: This daemon can easily force an out-of-memory condition since the data is not written
# to the CSV file as it's gathered - rather it's all stored in RAM until the data gathering
# time period has elapsed.
class LoggerDaemon(threading.Thread):
    log = None
    def __init__(self):
        threading.Thread.__init__(self)
	self.setDaemon(True)
	self.log = logging.getLogger('digilogger')		

    def run(self):
	self.log.debug("LoggerDaemon started.")
	canlogging_process()
	self.log.debug("LoggerDaemon exited.")

# Grab data and store in CSV
def canlogging_process():
	log_data_to_file = "can/data/runtime.txt"
	#ms_to_record = 60000 * 3			# 3 Minutes
	ms_to_record = 30
	records = []

	while (ms_to_record - time.clock()) > 0:
		data = []
		#print(ms_to_record - time.clock())
		data.append(time.clock())
		# Grab a "line" of data
		for param in canbus.PIDcodes:
			data.append(canbus.CANdata[param])
		
		records.append(data)
		
	with open(log_data_to_file, 'wb') as csvfile:
       		csv_writer = csv.writer(csvfile, delimiter=",", quotechar="|")
	
		for line in records:
			csv_writer.writerow(line)
