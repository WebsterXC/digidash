#################################################
#   ======    =====    ======   =====
#   ||	 \\     |     //	  |
#   ||    \\    |    // 	  |
#   ||    //    |    ||  =====	  |   --------
#   ||   //     |    \\     //	  |
#   ======    =====   ======    =====
##################################################

# [Summary]: This file manages and abstracts the communication with the ELM327 dongle. Using a Bluetooth
# socket, the Blue class manages the sending and receiving of characters through the ELM327 command set.
# Whether the command be for the underlying vehicle or the dongle itself, the ELM327 chip expects to
# receive ASCII characters. There are many possible return statements from the ELM327 dongle that
# aren't valid data; a set of exceptions is provided to handle the specific events.

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
    myMAC = "00:1D:A5:68:98:8A" # ELM327 Bluetooth Dongle MAC Address

    state = 0  # state is 1 if connected, 0 if disconnected
    sock = None
    delay = 0.005
    log = None

    def __init__(self):
	self.log = logging.getLogger('digilogger')
        print("Bluetooth object generated.")

    # Create a bluetooth socket with the MAC address provided
    def connect(self):
        if self.state == 1:
            raise StateError("Can't connect. You're already connected.")

        print("Opening Bluetooth socket...")
        count = 0
	# Try to open a bluetooth socket 5 times, spaced 5 seconds apart before giving up completely.
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

    # Disconnect from the open socket, if one is connected.
    def disconnect(self):
        if self.state == 0:
            raise StateError("Can't disconnect. You aren't connected.")
        self.state = 0
        self.sock.close()
	self.log.debug(''.join(("Connection with ", myMAC, "closed.")) )

    # Send characters to the ELM327 dongle and grab <=64 response characters.
    def send_recv(cmd):
        sock.send(cmd + "\r\n")
        time.sleep(0.005)
        
        while 1:
            c = sock.recv(64)
            nocarriage = c.replace('\r', "")
            buffer = nocarriage.replace('>', "")

	    # Handle erronous responses
            if buffer != "" and buffer != cmd:
                if buffer == "SEARCHING...":
                    continue
                if buffer == "?":
                    self.log.debug(''.join(("Command ", cmd, " is invalid.")))
                    raise InvalidCmdError("Command '%s' is invalid." % cmd)
                if buffer == "NO DATA":
                    self.log.debug(''.join(("Command ", cmd, " produced NO DATA.")))
                    raise NoDataError("Dongle returned 'NO DATA'.")
                if buffer == "STOPPED":
                    self.log.warning(''.join(("ELM returned STOPPED")))
                    raise StoppedError("Dongle returned 'STOPPED'.")
                if buffer == "UNABLE TO CONNECT":
                    self.log.warning(''.join(("ELM returned UNABLE TO CONNECT")))
                    raise StoppedError("Dongle returned 'UNABLE TO CONNECT'")
                return buffer
