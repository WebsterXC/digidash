import string
import time
import bluetooth #if you get an import error, then "sudo apt-get install python-bluez"

def send_recv(cmd): #send cmd parameter and return dongle response (ignores echoes)
    sock.send(cmd + "\r\n")
    time.sleep(0.005)
    c = sock.recv(64)
    nocarriage = c.replace('\r', " ")
    final = nocarriage.replace('>', " ")

    return final

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
res = send_recv("atz")
print("atz response is:")
print(res)

#-------------------
#SEND COMMAND "ate0" to turn echoes off
res = send_recv("ate0")
print("ate0 response is:")
print(res)

#-------------------
#RPM LOOP
while 1:
    res = send_recv("010C")
    '''
    print("Should be RPM. Response is:")
    '''
    data = res.split()
    if len(data) > 3:
        try:
    	    a = int(data[2], 16)
    	    b = int(data[3], 16)
        except ValueError:
            continue		
    else:
        continue

    rpm = ((256 * a) + b) / 4
    print("RPM is:")
    print(rpm)
    #time.sleep(1)

sock.close()
