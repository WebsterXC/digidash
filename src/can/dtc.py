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

	dtcstr = canbus.send_command(pids.MODE_DTC, "0x00")	

	# Get bytes in a list
	dtc_list = dtcstr.split()
	numfaults = len(dtc_list) / 2	

	print("Raw DTC return:")
	print(dtc_list)
	log.info(''.join(("DTC scan returned ", numfaults, " fault codes.")) )
	log.debug(''.join(("DTC request: ", dtcstr)) )

	dtc_codes = []
	iterator = 0
	while iterator < len(dtc_list)-1:
		# Each DTC code takes 2 bytes (2 list items) to represent
		firstbyte = dtc_list[iterator]
		secondbyte = dtc_list[iterator+1]

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
		subsystem += second
		subsystem += third
		subsystem += fourth
		subsystem += fifth
		dtc_codes.append(subsystem)
		
		# Increment by "2 bytes"
		iterator += 2	
	
	print("Generated codes: ")
	print(dtc_codes)

	return dtc_codes

# Clear all DTCs, including the check-engine light.
def dtc_clear():
	canbus.send_command(pids.MODE_DTC_CLR, "0x00")
	time.sleep(0.5)		# Buffer to ensure all clearing has been completed on vehicle-side.
	return
