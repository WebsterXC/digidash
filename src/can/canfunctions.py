# TODO: Find an accurate value for torque in Nm. (TORQUE_REF * TORQUE_ACT)?
#	Establish good thresholds for the waitfor_ functions


import logging
import time
import canbus, pids

## Blocking functions that wait for specific engine events. ##

# Wait for engine idle (no throttle and low RPM)
def waitfor_idle(name):
	log = logging.getLogger('digilogger')
	div_counter = 0	

	# Wait for "Idle"
	while canbus.CANdata[pids.ENG_RPM] > 900 and canbus.CANdata[pids.THROTTLE_REQ] > 2:
		# Do nothing.
		if div_counter % 25 == 0:
			log.debug(''.join( ("(", name, ") ", "Waiting for idle [", str(div_counter), "]")) )

		div_counter += 1
		continue

	return

# Wait for acelleration from standstill
def waitfor_accel(name):
	log = logging.getLogger('digilogger')
	div_counter = 0	
	
	# Idle reached. Now we need to wait until the user starts their pull.
	while canbus.CANdata[pids.THROTTLE_REQ] < 2:
		# Do nothing.
		if div_counter % 25 == 0:
			log.debug(''.join( ("(", name, ") ", "Waiting for pull start [", str(div_counter), "]")) )
		div_counter += 1
		continue
	
	return

# Wait for vehicle to reach 0 MPH
def waitfor_mph(name):
	log = logging.getLogger('digilogger')
	div_counter = 0	
	
	# Idle reached. Now we need to wait until the user starts their pull.
	while canbus.CANdata[pids.SPEED] < 2:
		# Do nothing.
		if div_counter % 25 == 0:
			log.debug(''.join( ("(", name, ") ", "Waiting for 0 MPH [", str(div_counter), "]")) )
		div_counter += 1
		continue
	
	return
	
#######################################################################################3

## DigiDash User Functions ##

# Begins a 3rd/4th gear dyno run simulation. Data is gathered during the pull and horsepower for each data
# point is calculated after the pull.
def dynopull_func(redline):
	pull_data = []
	dyno_data = []

	log = logging.getLogger('digilogger')
	log.debug("Beginning dyno pull test.")

	# Wait for vehicle idle
	waitfor_idle("Dynopull")

	# Then wait for driver to start the pull.
	waitfor_accel("Dynopull")	
	
	log.debug("Pull started...")

	# Acelleration started. Start gathering the RPM and actual measured torque
	while canbus.CANdata[pids.ENG_RPM] < redline:
		pull_data.append( (canbus.CANdata[pids.ENG_RPM], canbus.CANdata[pids.ENG_TORQUE_ACT]) )
		continue	# Do not remove -> data will not be appended to list.
	
	log.debug("Pull finished. Calculating horsepower...")

	# User has reached their specified redline. Test over. Calulate horsepower for graphing.
	for data in pull_data:
		# Tuple: (RPM, Torque, Horsepower)
		dyno_data.append( (data[0], data[1], pids.horsepower_calc(data[1], data[0])) )

	log.debug("Exiting dyno pull test.")

	return dyno_data


# Begin a full spectrum measurement of RPM/Torque across all gears. DigiDash will calculate the optimal
# upshift point for each gear.
def upshift_func():
	print("upshift function not implemented")


#Zero to sixty MPH timing function
def zerosixty_func():
	speed = 0
	cutoff = pids.units_kmh(60)

	log = logging.getLogger('digilogger')
	log.debug("Beginning 0-60 time test.")

	waitfor_mph("Zerosixty")
	log.debug("Pull started.")

	begin = time.clock()
	while speed < cutoff:
		speed = canbus.CANdata[pids.SPEED]

	elapsed = time.clock() - begin

	return elapsed 	

# Calculates quarter mile time and approximates horsepower based on speed. Requires vehicle weight for horsepower calculation.
def quartermile_func(weight):
	distance = 0
	finishline = 0.402336	# 0.25 miles to kilometers

	log = logging.getLogger('digilogger')
	log.debug("Beginning 0-60 time test.")

	# Wait for 0 MPH
	waitfor_mph("QMile")

	# Wait for start
	waitfor_accel("QMile")
	
	log.debug("Pull started.")

	# Fyzix. Distance (km)  = Velocity (km/h) * time(h) 
	stopwatch = 0
	distance = 0
	speed = 0

	while distance < finishline:
		clk = time.clock()			# Get time now
		speed = canbus.CANdata[pids.SPEED]	# Get current speed
		
		elapsed = time.clock() - clk		# Get elapsed time
		distance += ( (elapsed/3600) * speed )	# Calculate and add distance traveled (convert seconds to hours)
		stopwatch += elapsed			# Update total time of pull
	
	# Final speed used to approximate horsepower. Use -1 if weight is not available.
	if weight != -1:
		hp = pids.quartermile_calc(weight, pids.units_kmh(speed))
	else:
		hp = -1

	log.debug(''.join( ("Quartmile test finished with a time of ", stopwatch, "s, with approx. ", hp, " horsepower.")) )

	return (stopwatch, hp)
