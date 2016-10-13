import time
import pids
from daemon import ParserDaemon

d = ParserDaemon()
d.start()

for i in range(0, 100):
    print( d.get_data(0x0C) )
    time.sleep(0.25)
