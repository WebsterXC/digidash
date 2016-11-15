# Various vehicle tests / dyno simulation

from can import canbus, pids

# Begins a 3rd/4th gear dyno run simulation. Data is gathered, calculated, and interpolated to return a set
# of data fit for plotting.
def dyno_pull(redline):
	dyno_data = []

	# Wait for "Idle"
	while canbus.CANdata[pids.ENG_RPM] > 900:
		# Do nothing.
		continue

	while canbus.CANdata[pids.ENG_RPM] < redline:
		dyno_data.append( (canbus.CANdata[pids.ENG_RPM], canbus.CANdata[pids.ENG_TORQUE_ACT]) )
		continue	# Do not remove: WB
	
	return dyno_data


# Begin a full spectrum measurement of RPM/Torque across all gears. DigiDash will calculate the optimal
# upshift point for each gear.
