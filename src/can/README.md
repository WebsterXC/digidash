# Backend Notes #

### Daemons ###
Daemons are background threads that ensure tasks happen in the background without affecting the usability of the front end (GUI, etc). All daemons
have their own class associated with them and can be imported individually.

##### ParserDaemon #####
This daemon simulates live data coming from the vehicle. Using a comma delimited text file, the thread uses the RTES parameter to ensure that
simulated data is placed in it's data structure at the correct time. The Parser's get_data method is passed a PID and retrieves the most recent
parameter value.

The Parser Daemon can be invoked as follows:

	from daemon import ParserDaemon
	d = ParserDaemon()			# Create the Daemon
	d.start()				# Start the Daemon

After creating and starting it, use the daemon's get_data method to read data:

	for i in range(0, 100):
    		print( d.get_data(0x0C) )
    		time.sleep(0.25)			# Read every 0.25 seconds (optional)

ParserDaemon currently has no way of stopping itself, so the thread only lasts for 2 runthroughs of the CSV file. To exit prematurely,
use CTRL+Z.
