# Background daemons and coordinate data gathering/computation in various ways.
import time
import threading
import csv
import canbus, pids
import automath
import logging

csv_file = 'can/data/data.txt'                                  # Sample data file to open
inparams = ["0x1F", "0x0C", "0x0D", "0x0F", "0x0B", "0x10", "0x11", "0x5D"] # Columns in sample data CSV

#inparams = [pids.ENG_RPM, pids.SPEED, pids.THROTTLE_REQ, pids.ENG_TORQUE_REF, pids.ENG_TORQUE_ACT]

# Parser daemon is used for DEVELOPMENT ONLY. Reads recorded data from a CSV file and
# places it in the central data structure. It ensures data is in the structure at
# the time listed in the CSV file by establishing a time quantum after looking at the
# delay to the next input data row.
class ParserDaemon(threading.Thread):
    log = None
    def __init__(self):
        threading.Thread.__init__(self)
	self.setDaemon(True)
	self.log = logging.getLogger('digilogger')

    def run(self):
        # Initialisation
        for i in range(0,101):
            canbus.CANdata[i] = -1     #Optional
      
	self.log.debug('Parser process starting...')            
 
        # Begin reading data
        parser_process()

	self.log.debug('Parser process finished.')            

    # Return a piece of data given a PID code
    def get_data(self, dat):
        return canbus.CANdata.get(dat)

def parser_process():
        exitflag = False                # Exits on True

        # 100 readthroughs of data file as a max timeout
        for i in range(0, 100):
            with open(csv_file, 'rb') as csvf:  # Open the file
                # csv_reader is an iterator and only contains 1 line at a time
                csv_reader = csv.reader(csvf, delimiter=",", quotechar="|")
            
                # Read the first line for data
                data_row = csv_reader.next()

                # Read the second line for time reference
                time_row = csv_reader.next()

                # While time_row is not an empty list
                while time_row:
                    
                    # Place data from row in CAN dictionary
                    counter = 0
                    for param in data_row:
			canbus.CANlock.acquire()
			canbus.CANdata[inparams[counter]] = float(param)
			canbus.CANlock.release()
			counter += 1
			

                    # Establish time quantum and wait
                    time_now = float(data_row[0])
                    time_later = float(time_row[0])
                    time.sleep(time_later - time_now)

                    # Iterative housekeeping
                    data_row = time_row
                    time_row = csv_reader.next()

# Daemon handles gathering of engine parameters from canbus.PIDcodes
class CANDaemon(threading.Thread):
    log = None
    def __init__(self):
        threading.Thread.__init__(self)
	self.setDaemon(True)
	self.log = logging.getLogger('digilogger')		

    def run(self):
        # Begin reading data
	self.log.debug("CAN Daemon started...")
        can_process()
	self.log.debug("CAN Daemon finished.")

def can_process():
	while 1:
		# Iterate through PIDcodes and get data for each. Place in CANdata.
		for pid in canbus.PIDcodes:
			answer = canbus.send_pid(pid)

			canbus.CANlock.acquire()
			canbus.CANdata[pid] = automath.convert(pid, answer)
			canbus.CANlock.release()
			time.sleep(0)	# Yield

# Daemon logs engine data to a CSV .txt file
class LoggerDaemon(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
	#self.setDaemon(True)

    def run(self):
	canlogging_process()

# Grab data and store in CSV
def canlogging_process():
	log_data_to_file = "can/data/runtime.txt"
	#ms_to_record = 60000 * 3			# 3 Minutes
	ms_to_record = 1
	
	with open(log_data_to_file, 'wb') as csvfile:
        	csv_writer = csv.writer(csvfile, delimiter=",", quotechar="|")

		while (ms_to_record - time.clock()) > 0:
			data = []
			# Grab a "line" of data
			for param in canbus.PIDcodes:
				data.append(canbus.CANdata[param])

			# Write to CSV
			csv_writer.writerow(data)	
