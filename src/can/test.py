import canbus
import daemon
import time

# NOTE: This test requires sudo rfcomm0 <:mac:> (see Slack).

# Create canbus object. This also initiates a connection with the bluetooth receiver.
c = canbus.canbus()

# Create CAN daemon and start it.
d = daemon.CANDaemon()
d.start()

# Read vehicle data from the canbus dictionary that the CANDaemon is updating in the background.
while 1:
	print(canbus.CANdata)
	time.sleep(0.1)

        # Known Bugs: Only 2-3 runs of this program (test.py) are possible before needing to restart. This is probably because I never formally
        #             close the connection between the RPi and Bluetooth dongle.

        #             Eventually, this while loop will secretly time-out. After about 20-30 seconds, the CANDaemon starts receiving constant 'NO DATA'
        #             bytes from the Bluetooth dongle, but won't notify you in any way, so the data stream being printed to the screen eventually becomes
        #             stale. I'm 99% confident socket programming will solve this bug, which is the planned implementation.
