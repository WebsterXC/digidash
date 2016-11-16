from daemon import CANDaemon
import canbus, pids
import time

c = canbus.canbus()

# Uncomment for automatically grabbed pids
#d = CANDaemon()
#d.start()

for i in range(0, 100):
	# Grab automatically updated PID
	rpm = canbus.CANdata[pids.ENG_RPM]

	# Manually request PID
	demand = canbus.send_pid(pids.ENG_TORQUE_DMD)
	actual = canbus.send_pid(pids.ENG_TORQUE_ACT)
	reference = canbus.send_pid(pids.ENG_TORQUE_REF)

	print( rpm )
	print( [demand, actual, reference] )

	time.sleep(0.1)
