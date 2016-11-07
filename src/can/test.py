from daemon import ParserDaemon
import canbus
import time

d = ParserDaemon()
d.start()

for i in range(0, 10):
	print( d.get_data(0x0C) )
	time.sleep(0.25)
