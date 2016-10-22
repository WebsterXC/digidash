import string
import time
import bluetooth #if you get an import error, then "sudo apt-get install python-bluez"

def send_recv(cmd): #send cmd parameter and return dongle response (ignores echoes)
    sock.send(cmd + "\r\n")
    time.sleep(0.1)
    while 1:
        buffer = ""
        while 1:
            c = sock.recv(1)
            #print("c is:%s:", c)
            if c == '\r' and len(buffer) > 0:
                break
            else:
                if buffer != "\r" and c != ">":
                    buffer = buffer + c
        #print("Here!")
        print(buffer)
        if buffer != "" and buffer != "\r" and buffer != cmd and buffer != (">" + cmd):
            return buffer

myMAC = "00:1D:A5:00:03:4E" #Mark's dongle (ELM v1.5 aka shit chinese clone)
#myMAC = ":::::" #Will's dongle (ELM v2.1 aka not CHINA CHINA CHINA)
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
res = send_recv("atz")
print("atz response is:")
print(res)

#-------------------
#SEND COMMAND "ate0" to turn echoes off
res = send_recv("ate0")
print("ate0 response is:")
print(res)

#-------------------
#SEND COMMAND "0100" to ready dongle for communication
res = send_recv("0100")
print("0100 response is:")
print(res)

#-------------------
#RPM LOOP
while 1:
    res = send_recv("010C")
    print("Should be RPM. Response is:")
    print(res)
    data = res.split()
    a = int(data[2], 16)
    b = int(data[3], 16)
    rpm = ((256 * a) + b) / 4
    print("RPM is %d" % rpm)
    time.sleep(1)

sock.close()
