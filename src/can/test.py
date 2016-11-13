from daemon import CANDaemon
import canbus
import time

c = canbus.canbus()

d = CANDaemon()
d.start()

for i in range(0, 10):
	print( canbus.CANdata )
	time.sleep(0.2)
