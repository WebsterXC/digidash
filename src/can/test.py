import canbus
import daemon
import time

c = canbus.canbus()


d = daemon.CANDaemon()
d.start()

while 1:
	print(canbus.CANdata)
	time.sleep(0.1)
