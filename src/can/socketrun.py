import string
import time
import bluetooth #if you get an import error, then "sudo apt-get install python-bluez"
import dtc

def send_recv(cmd, respSize): #send cmd parameter and return dongle response (ignores echoes)
    sock.send(cmd + "\r\n")
    time.sleep(0.005)
    resp1 = ""
    while(1):
        if respSize == 0:  #if 0, expected response size not known
            resp1 = sock.recv(32)
            resp1 = resp1.replace('\r', "")
            resp1 = resp1.replace('>', "")
            if resp1 == "SEARCHING...":
                continue
            '''if resp1 == "?":
                self.log.info(''.join(("Command ", cmd, " is invalid.")))
                raise InvalidCmdError("Command '%s' is invalid." % cmd)
            if resp1 == "NO DATA":
                self.log.info(''.join(("Command ", cmd, " produced NO DATA.")))
                raise NoDataError("Dongle returned 'NO DATA'.")
            if resp1 == "STOPPED":
                self.log.info(''.join(("ELM returned STOPPED")))
                raise StoppedError("Dongle returned 'STOPPED'.")
            if resp1 == "UNABLE TO CONNECT":
                self.log.warning(''.join(("ELM returned UNABLE TO CONNECT")))
                raise StoppedError("Dongle returned 'UNABLE TO CONNECT'") '''
            return resp1
        else:
            break
    while(1):
        resp2 = sock.recv(32)
        resp2 = resp2.replace('\r', "")
        resp2 = resp2.replace('>', "")
        resp1 += resp2
        data = resp1.split()
        if len(data) == 1:
            if data[0] == "SEARCHING...":
                continue
            '''if data[0] == "?":
                self.log.info(''.join(("Command ", cmd, " is invalid.")))
                raise InvalidCmdError("Command '%s' is invalid." % cmd)
            if data[0] == "STOPPED":
                self.log.info(''.join(("ELM returned STOPPED")))
                raise StoppedError("Dongle returned 'STOPPED'.") '''
            if respSize == 1:
                print("How did I get here? Cmd was '"+cmd+"' and response was '"+resp1+"'.")
                return resp1
        elif len(data) == 2:
            '''if resp1 == "NO DATA":
                self.log.info(''.join(("Command ", cmd, " produced NO DATA.")))
                raise NoDataError("Dongle returned 'NO DATA'.") '''
            if respSize == 2:
                return resp1
        elif len(data) == 3:
            '''if resp1 == "UNABLE TO CONNECT":
                self.log.info(''.join(("ELM returned UNABLE TO CONNECT")))
                raise StoppedError("Dongle returned 'UNABLE TO CONNECT'") '''
            if respSize == 3:
                return resp1
        elif len(data) == respSize:
            return resp1
        elif len(data) > respSize:
            print("How did I get here? Cmd was '"+cmd+"' and response was '"+resp1+"'.")
            '''self.log.info(''.join(("ELM returned too large of a response")))
            raise ResponseError("Dongle returned too large of a response")'''
            return "40 10 00 00"
            

#myMAC = "00:1D:A5:00:03:4E" #Mark's dongle (ELM v1.5 aka shit chinese clone)
myMAC = "00:1D:A5:68:98:8A" #Will's dongle (ELM v2.1 aka not CHINA CHINA CHINA)
print("Opening Bluetooth socket...")

while 1:
    try:
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((myMAC, 1))
        break
    except bluetooth.btcommon.BluetoothError as error:
        sock.close()
        print ("Could not connect: ", error, "; Retrying in 5 seconds...")
        time.sleep(5)

print("Socket successfully opened!")

#-------------------
#SEND COMMAND "atz" to clear all
res = send_recv("atz", 2)
print("atz response is:")
print(res)

#-------------------
#SEND COMMAND "ate0" to turn echoes off
res = send_recv("ate0", 1)
print("ate0 response is:")
print(res)

#-------------------
#RPM LOOP

while 1:
    res = send_recv("010C", 4)
    print("RPM response is:")
    print(res)
    data = res.split()
    a = int(data[2], 16)
    b = int(data[3], 16)
    rpm = ((256 * a) + b) / 4
    print("RPM is:")
    print(rpm)

sock.close()
