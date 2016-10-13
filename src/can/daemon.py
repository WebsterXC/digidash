# Background daemons and coordinate data gathering/computation in various ways.
import time
import threading
import csv

csv_file = 'data/data.txt'                                  # Sample data file to open
CANData = { }                                               # CAN Dictionary (will change once data structure is setup elsewhere)
inparams = [0x1F, 0x0C, 0x0D, 0x0F, 0x0B, 0x10, 0x11, 0x5D] # Columns in sample data CSV

# Parser daemon is used for DEVELOPMENT ONLY. Reads recorded data from a CSV file and
# places it in the central data structure. It ensures data is in the structure at
# the time listed in the CSV file by establishing a time quantum after looking at the
# delay to the next input data row.
class ParserDaemon(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        # Initialisation
        for i in range(0,101):
            CANData[i] = -1
       
        # Begin reading data
        parser_process()

    # Return a piece of data given a PID code
    def get_data(self, dat):
        return CANData.get(dat)

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
                        CANData[inparams[counter]] = float(param)
                        counter += 1


                    # Establish time quantum and wait
                    time_now = float(data_row[0])
                    time_later = float(time_row[0])
                    time.sleep(time_later - time_now)

                    # Iterative housekeeping
                    data_row = time_row
                    time_row = csv_reader.next()


# Please ignore what's below.
'''
# Daemon is used to constantly monitor vehicle parameters to identify inconsistencies,
# sudden DTC codes and record complex data sets (torque curves, etc).
def daemon_monitor(self):
    return 0

# ENTRY POINT
daemon_parser()

for i in range(0, 10):
    printout = []
    for element in inparams:
        printout.append(CANData[element])

    print(printout)
    time.sleep(0.25)
'''
