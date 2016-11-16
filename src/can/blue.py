# File defines methods to interact with the OBDII bluetooth receiver.
# Used https://github.com/Pbartek/pyobd-pi and https://github.com/peterh/pyobd as guides
# The OBD-II bluetooth reader we are deploying uses ELM327 protocol to communicate.

import logging
import string
import time
import bluetooth #if you get an import error, then "sudo apt-get install python-bluez"

class ConnectFailureError(Exception):
    pass

class StateError(Exception):
    pass

class InvalidCmdError(Exception):
    pass

class NoDataError(Exception):
    pass

class StoppedError(Exception):
    pass

class Blue:
    #myMAC = "00:1D:A5:00:03:4E"  # Mark's dongle (ELM v1.5 aka shit chinese clone)
    myMAC = "00:1D:A5:68:98:8A" #Will's dongle (ELM v2.1 aka not CHINA CHINA CHINA)

    state = 0  # state is 1 if connected, 0 if disconnected
    sock = None
    delay = 0.017 #WE NEED TO TEST THIS VALUE!!! 11/6
    log = None

    def __init__(self):
	self.log = logging.getLogger('digilogger')
        print("Bluetooth object generated.")

    def connect(self):
        if self.state == 1:
            raise StateError("Can't connect. You're already connected.")

        print("Opening Bluetooth socket...")
        count = 0
        while 1:
            try:
                self.state = 1
                self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                self.sock.connect((self.myMAC, 1))
                break
            except bluetooth.btcommon.BluetoothError as error:
                self.state = 0
                self.sock.close()
                count += 1
                if count == 5:
		    self.log.critical("Failed to open socket connection.")
                    raise ConnectFailureError("Connect failed 5 times. I give up.")
                print ("Could not connect: ", error, "; Retrying in 5 seconds...")
                time.sleep(5)
        print("Socket successfully opened!")
	self.log.debug(''.join(("Socket connected with ", myMAC)) )

    def disconnect(self):
        if self.state == 0:
            raise StateError("Can't disconnect. You aren't connected.")
        self.state = 0
        self.sock.close()
	self.log.debug(''.join(("Connection with ", myMAC, "closed.")) )

    def send_recv(self, cmd):  # send cmd parameter and return dongle response (ignores echoes)
        if self.state == 0:
            raise StateError("Can't send/recv. You aren't connected.")
        self.sock.send(cmd + "\r\n")
        time.sleep(self.delay)
        while 1:
            buffer = ""
            while 1:
                c = self.sock.recv(1)
                #print("c is:%s:", c)
                if (c == '\r' or c == '>') and len(buffer) > 0:
                    break
                else:
                    if c != "\r" and c != ">":
                        buffer = buffer + c
            # print("Here!")
            # print(buffer)
            if buffer != "" and buffer != "\r" and buffer != cmd and buffer != (">" + cmd):
                if buffer == "SEARCHING...":
                    continue
                if buffer == "?":
		    self.log.debug(''.join(("Command ", cmd, " is invalid.")) )
                    raise InvalidCmdError("Command '%s' is invalid." % cmd)
                if buffer == "NO DATA":
		    self.log.debug(''.join(("Command ", cmd, " produced NO DATA.")) )
                    raise NoDataError("Dongle returned 'NO DATA'.")
                if buffer == "STOPPED":
		    self.log.warning(''.join(("ELM returned STOPPED")) )
                    raise StoppedError("Dongle returned 'STOPPED'.")
                sock.recv(2) # get rid of "\r>" that's still waiting to be received
                #print("Response is")
                #print(buffer)
                return buffer
