# File defines methods to interact with the OBDII bluetooth receiver.
# Used https://github.com/Pbartek/pyobd-pi and https://github.com/peterh/pyobd as guides
# The OBD-II bluetooth reader we are deploying uses ELM327 protocol to communicate.

import string
import time
import bluetooth #if you get an import error, then "sudo apt-get install python-bluez"

class Blue:
    #myMAC = "00:1D:A5:00:03:4E"  # Mark's dongle (ELM v1.5 aka shit chinese clone)
    myMAC = "00:1D:A5:68:98:8A" #Will's dongle (ELM v2.1 aka not CHINA CHINA CHINA)

    state = 0  # state is 1 if connected, 0 if disconnected
    sock = None
    delay = 0.017

    def __init__(self):
        print("Bluetooth object generated.")

    def connect(self):
        if self.state == 1:
            print("You're already connected!")
            return

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
                if ++count == 5:
                    raise Exception("Connect failed 5 times. I give up.")
                print ("Could not connect: ", error, "; Retrying in 5 seconds...")
                time.sleep(5)
        print("Socket successfully opened!")

    def disconnect(self):
        self.state = 0
        self.sock.close()

    def send_recv(self, cmd):  # send cmd parameter and return dongle response (ignores echoes)
        if self.state == 0:
            raise Exception("You aren't connected.")
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
                else:                
                    sock.recv(2) # get rid of "\r>" that's still waiting to be received
                    #print("Response is")
                    #print(buffer)
                    return buffer
