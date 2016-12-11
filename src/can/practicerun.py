# File defines methods to interact with the OBDII bluetooth receiver.
# Used https://github.com/Pbartek/pyobd-pi and https://github.com/peterh/pyobd as guides

# The OBD-II bluetooth reader we are deploying uses ELM327 protocol to communicate.

import serial
import string
import time

baud = 9600
databits = 8
par = serial.PARITY_NONE  # parity
sb = 1  # stop bits
to = 0.5 # 500 millisecond timeout period for read()
ELMver = "Unknown"
State = 1  # state SERIAL is 1 connected, 0 disconnected (connection failed)

print("Opening serial connection...")

try:    #note: this next line opens port
    port = serial.Serial("/dev/rfcomm0", baud, parity=par, stopbits=sb, bytesize=databits, timeout=to)

except serial.SerialException as e:
    print e
    State = 0
    print ("Damn! Couldn't open the connection.")

#-------------------
#SEND COMMAND "atz" to clear all
#The 'atz' command is used to retrieve the ELM version of the Bluetooth Dongle. 
if port:
    port.flushOutput()
    port.flushInput()
    for c in "atz":
        port.write(c) #writes to port in characters
    port.write("\r\n")
else:
    print("Can't send command.")
print("atz sent.")
#-------------------
#GET RESULT
time.sleep(0.1)
if port:
    buffer = ""
    while 1:
        c = port.read(1)
        if c == '\r' and len(buffer) > 0:
            break
        else:
            if buffer != "" or c != ">": #if something is in buffer, add everything
                buffer = buffer + c
        #ELMver = buffer
else:
    print("No Port! Can't get result.")
print("Should be echo. Buffer is:")
print(buffer)
#-------------------
#GET RESULT
time.sleep(0.1)
if port:
    buffer = ""
    while 1:
        c = port.read(1)
        if c == '\r' and len(buffer) > 0:
            break
        else:
            if buffer != "" or c != ">": #if something is in buffer, add everything
                buffer = buffer + c
        #ELMver = buffer
else:
    print("No Port! Can't get result.") #displayed if the port is empty
print("Should be ELM version. Buffer is:") #ELM 2.1 is found to be compatible with the project
print(buffer)

#-------------------
#SEND COMMAND "ate0" to turn echo off
if port:
    port.flushOutput()
    port.flushInput()
    for c in "ate0":
        port.write(c) #sends commands in characters
    port.write("\r\n")
else:
    print("Can't send command.")
print("ate0 sent.")
#-------------------
#GET RESULT
time.sleep(0.1)
if port:
    buffer = ""
    while 1:
        c = port.read(1)
        if c == '\r' and len(buffer) > 0:
            break
        else:
            if buffer != "" or c != ">": #if something is in buffer, add everything
                buffer = buffer + c
        #ELMver = buffer
else:
    print("No Port! Can't get result.")
print("Should be echo. Buffer is:")
print(buffer)

#-------------------
#SEND COMMAND "0100" to ready dongle for communication
#This command initializes the bluetooth dongle to send and receive commands from the user
if port:
    port.flushOutput()
    port.flushInput()
    for c in "0100":
        port.write(c)
    port.write("\r\n")
else:
    print("Can't send command.")
print("0100 sent.")

#-------------------
#GET RESULT
time.sleep(0.1)
if port:
    buffer = ""
    while 1:
        c = port.read(1)
        if c == '\r' and len(buffer) > 0:
            break
        else:
            if buffer != "" or c != ">": #if something is in buffer, add everything
                buffer = buffer + c
else:
    print("No Port! Can't get result.")
print("Should say 41 00 BE 1F B8 10 or the like. Buffer is:") #expected output from dongle
print(buffer) #displays actual output from dongle in HEX
#-------------------

#-------------------
#RPM LOOP
while 1:
    if port:
        port.flushOutput()
        port.flushInput()
        for c in "010C": #command to request RPM values from the bluetooth dongle 
            port.write(c)
        port.write("\r\n")
    else:
        print("Can't send command.")

    time.sleep(0.1)
    if port:
        buffer = ""
        while 1:
            c = port.read(1)
            if c == '\r' and len(buffer) > 0: #returns characters until the end of message
                break
            else:
                if buffer != "" or c != ">":  # if something is in buffer, add everything
                    buffer = buffer + c
    else:
        print("No Port! Can't get result.")
    print("Should be RPM. Buffer is:")
    print(buffer)
    #temp = eval("0x" + buffer, {}, {})
    data = buffer.split()
    a = int(data[2], 16) 
    b = int(data[3], 16)
    rpm = ((256*a) + b)/4 #computes the RPM value from data received from the dongle
    print("RPM is %d" % rpm)
    time.sleep(1)

port.close()
