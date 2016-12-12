#################################################
#   ======    =====    ======   =====
#   ||	 \\     |     //	  |
#   ||    \\    |    // 	  |
#   ||    //    |    ||  =====	  |   --------
#   ||   //     |    \\     //	  |
#   ======    =====   ======    =====
##################################################

# [Summary]: This file defines methods to interact with a vehicles diagnostic trouble
# code (DTC) subsystem. The DTC subsystem defines its own modes separate from realtime
# gathering and are therefore offered as nonclass methods.

import canbus, pids
import time, logging

sysmask	= 192 	# Bitmask for the first DTC character (P/C/B/U)
twomask = 48 	# Bitmask for second DTC character
threemask = 240 # Third DTC character
fourmask = 15 	# Fourth DTC character

# Request all trouble codes from the vehicle and return a list of trouble codes. This
# method returns DTCs in their standard format P/C/B/U + XXXX.
def dtc_scan():
	log = logging.getLogger('digilogger')

	# Pinging for all active DTC codes takes much longer than request a realtime
	# PID, and to compensate the ELM327 fills the return buffer with "SEARCHING..."
	# while it compiles the return list. Therefore, we call the send_command method
	# twice - the first time initiates the DTC scan and results in "SEARCHING...".
	# The second send_command function will returned the combined buffer (SEARCHING...
	# and the DTC scan response.
	dtcstr = canbus.send_command(pids.MODE_DTC, "0x00")	
	time.sleep(0.5)
	dtcstr = canbus.send_command(pids.MODE_DTC, "0x00")	

	dtc_list = dtcstr.split()	# List should always begin with: ["SEARCHING...", "43", "00"]
	if len(dtc_list) < 4:
		log.info("DTC scan returned no active fault codes.") #MIL status off
		return []

	dtc_list.pop(0)			# Remove "SEARCHING..."
	numfaults = len(dtc_list) / 2		
	log.info(''.join(("DTC scan returned ", str(numfaults), " fault codes.")) ) #displays the number of faults codes found 
	log.debug(''.join(("DTC request: ", dtcstr)) )

	dtc_codes = [] #stores DTC codes
	iterator = 2
	while iterator < len(dtc_list)-1:
		# Each DTC code takes 2 bytes (2 list items) to represent
		firstbyte = int(dtc_list[iterator], 16)
		secondbyte = int(dtc_list[iterator+1], 16)

		#Bit masking
		# Get all five DTC characters
		first = (firstbyte & sysmask) >> 6
		second = (firstbyte & twomask) >> 4
		third = (firstbyte & fourmask)
		fourth = (secondbyte & threemask) >> 4
		fifth = (secondbyte & fourmask)

		subsystem = " "
		if first == 0:
			subsystem = "P"
		elif first == 1:
			subsystem = "C"
		elif first == 2:
			subsystem = "B"
		elif first == 3:
			subsystem = "U"
		
		# Build the DTC trouble code
		subsystem += str(second)
		subsystem += str(third)
		subsystem += str(fourth)
		subsystem += str(fifth)
		dtc_codes.append(subsystem)
		
		# Increment by "2 bytes"
		iterator += 2	
	
	return dtc_codes

# Clear all DTCs, including the check-engine light. The ELM327 dongle will
# return NO DATA regardless of if the command was successful or not.
def dtc_clear():
	canbus.send_command(pids.MODE_DTC_CLR, "0x00") #MODE 4 clears DTC codes
	time.sleep(1)		# Buffer to ensure all clearing has been completed on vehicle-side.
	return
