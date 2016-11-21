#MIL Status
#number of DTC codes
#no support for actual DTC codes


import string
import time
import canbus


port = canbus.canbus();

#should print Bluetooth object generated

#exceptions already handled by blue.py

time.sleep(0.5) #half second delay

#-------------------
#SEND COMMAND "0100" to ready dongle for communication
if port:
    buffer = “”
    buffer = port.send_pid("0x00")
else:
    print("Can't send command.")

time.sleep(0.1) #delay
#echoes are already ignored
print(buffer) #should display HEX value

#dongle is now ready

#-------------------
MIL_status_check = 0;

while (MIL_status_check==0):
    if port:
        buffer = “”
        buffer = port.send_pid("0x01")
    else:
        print("Can't send command.")

    time.sleep(0.5) #delay
    #echoes are already ignored
print(“Raw bytes for MIL:”)
    print(buffer)
    
    data = buffer.split()
    #4 bytes are stored as BITS
    a = data[2]
    b = data[3]
    c = data[4]
    d = data[5]
        
        #MIL status and # of DTC codes
        a_copy_mil = hex_to_bin(a)
        print("a_copy_mil: ")
        print(a_copy_mil)
        a_copy_dtc_num = hex_to_bin(a)
        print("a_copy_dtc_num: ")
        print(a_copy_dtc_num)
                                
        a_copy_mil1 = a_copy_mil>>7 #right shift 7 bits
        a_copy_mil = a_copy_mil1<<7 #left shift 7 bits
                                        
        a_copy_dtc_num1 = a_copy_dtc_num << 1 #left shift 1 bit
        a_copy_dtc_num = a_copy_dtc_num1 >> 1 #right shift 1 bit
                                                
        mil_stat = int(a_copy_mil, 16)
        mil_stat_print  = 1*mil_stat
        print("mil_stat_print: ")
        print(mil_stat_print)
        dtc_num = int(a_copy_dtc_num, 16)
        dtc_num_print = 1*dtc_num


if(mil_stat_print==128): # if MIL is on, mil_stat_print will store an int value of 128
    print(“MIL is ON. :-( ”)
          print(“Number of DTC codes found: %d” % dtc_num_print)
          dtc_code_list = get_dtc_values(); 
          print(“The code is : “)
          print(dtc_code_list)
          else:
       	 	print(“MIL is OFF. :-)) “)
            
            MIL_status_check = 1
            print(“MIL status checked. Connection will now disconnect.”)
            time.sleep(1)

port.disconnect();
