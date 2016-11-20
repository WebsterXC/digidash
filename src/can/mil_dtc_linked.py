

# supports actual DTC description

import string
import time
import canbus
import dtc


port = canbus.canbus();
mil_dtc = dtc.dtc();

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
print(“\n”)
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
		dtc_code_list = get_dtc_values()
              dtc_dict_des = mil_dtc.dtc_dict[dtc_code_list] # retrieves dtc description from the dictionary
		print(“The code is : “)
		print(dtc_code_list)
              print(dtc_dict_des) #prints dtc description
	else:
       	 	print(“MIL is OFF. :-)) “)

    MIL_status_check = 1
    print(“MIL status checked. Connection will now disconnect.”)
    time.sleep(1)

port.disconnect();

#function 1
def get_dtc_values():

#ret_none = 0

if port:
    buffer = “”
    buffer = port.send_command("0x0300") #send_command only recognizes the 03 mode
else:
    print("Can't send command.")

time.sleep(0.1) #delay
#echoes are already ignored 
print(buffer) #should display HEX value

data = buffer.split()
    #stores data as HEX
    #each frame returns 4 bytes
    a = hex_to_bin(data[2]) # only 1st byte from 1st frame
    b = hex_to_bin(data[3]) # only 2nd byte from 1st frame

    #c = int(data[4], 16)
    #d = int(data[5], 16)

dtc_code_ = get_dtc_code(a,b)

return dtc_code_;



def get_dtc_code(first_second_third, forth_five):
 

by1 = first_second_third
print("by1: ")
print(by1)
by2 = forth_five
print("by2: ")
print(by2)

dtc_string = “”

a = by1
	
	a_bit7_6 = a>>5
	a_bit7_6 = a_bit7_6<<5
		if(a_bit7_6 == 0b00000000):
			dtc_string = ‘P’ #powertrain
		elif(a_bit7_6 == 0b01000000):
			dtc_string = ‘C’ #chassis
		elif(a_bit7_6 = 0b10000000):
			dtc_string = ‘B’ #body
		elif(a_bit7_6 = 0b11000000):
			dtc_string = ‘U’ #network		
	
	a_bit5_4 = a>>3
	a_bit5_4 = a_bit5_4<<3
	a_bit5_4 = a_bit5_4<<2
	a_bit5_4 = a_bit5_4>>2
        
		if(a_bit5_4 = 0b00000000):
			dtc_string = dtc_string + ‘0’
		elif(a_bit5_4 = 0b00010000):
			dtc_string = dtc_string + ‘1’
		elif(a_bit5_4 = 0b00100000):
			dtc_string = dtc_string + ‘2’
		elif(a_bit5_4 = 0b00110000):
			dtc_string = dtc_string + ‘3’		

	a_bit3_0 = a<<5
	a_bit3_0 = a_bit3_0>>5

		if(a_bit3_0 = 0b00000000):
			dtc_string = dtc_string + ‘0’
		elif(a_bit3_0 = 0b00000001):
			dtc_string = dtc_string + ‘1’
		elif(a_bit3_0 = 0b00000010):
			dtc_string = dtc_string + ‘2’
		elif(a_bit3_0 = 0b00000011):
			dtc_string = dtc_string + ‘3’
		elif(a_bit3_0 = 0b00000100):
			dtc_string = dtc_string + ‘4’
		elif(a_bit3_0 = 0b00000101):
			dtc_string = dtc_string + ‘5’
		elif(a_bit3_0 = 0b00000110):
			dtc_string = dtc_string + ‘6’
		elif(a_bit3_0 = 0b00000111):
			dtc_string = dtc_string + ‘7’
		elif(a_bit3_0 = 0b00001000):
			dtc_string = dtc_string + ‘8’
		elif(a_bit3_0 = 0b00001001):
			dtc_string = dtc_string + ‘9’
       elif(a_bit3_0 = 0b00001010):
            dtc_string = dtc_string + ‘A’
		elif(a_bit3_0 = 0b00001011):
			dtc_string = dtc_string + ‘B’
		elif(a_bit3_0 = 0b00001100):
			dtc_string = dtc_string + ‘C’
		elif(a_bit3_0 = 0b00001101):
			dtc_string = dtc_string + ‘D’
		elif(a_bit3_0 = 0b00001110):
			dtc_string = dtc_string + ‘E’
		elif(a_bit3_0 = 0b00001111):
			dtc_string = dtc_string + ‘F’


b = by2

b_bit7_4 = b>>4
b_bit7_4 = b_bit7_4<<4

		if(b_bit7_4 = 0b00000000):
			dtc_string = dtc_string + ‘0’
		elif(b_bit7_4 = 0b00010000):
			dtc_string = dtc_string + ‘1’
		elif(b_bit7_4 = 0b00100000):
			dtc_string = dtc_string + ‘2’
		elif(b_bit7_4 = 0b00110000):
			dtc_string = dtc_string + ‘3’
		elif(b_bit7_4 = 0b01000000):
			dtc_string = dtc_string + ‘4’
		elif(b_bit7_4 = 0b01010000):
			dtc_string = dtc_string + ‘5’
		elif(b_bit7_4 = 0b01100000):
			dtc_string = dtc_string + ‘6’
		elif(b_bit7_4 = 0b01110000):
			dtc_string = dtc_string + ‘7’
		elif(b_bit7_4 = 0b10000000):
			dtc_string = dtc_string + ‘8’
		elif(b_bit7_4 = 0b10010000):
			dtc_string = dtc_string + ‘9’
        elif(b_bit7_4 = 0b10100000):
            dtc_string = dtc_string + ‘A’
		elif(b_bit7_4 = 0b10110000):
			dtc_string = dtc_string + ‘B’
		elif(b_bit7_4 = 0b11000000):
			dtc_string = dtc_string + ‘C’	
		elif(b_bit7_4 = 0b11010000):
			dtc_string = dtc_string + ‘D’
		elif(b_bit7_4 = 0b11100000):
			dtc_string = dtc_string + ‘E’
		elif(b_bit7_4 = 0b11110000):
			dtc_string = dtc_string + ‘F’	

b_bit3_0 = b<<4
b_bit3_0 = b_bit3_0>>4

		if(b_bit3_0 = 0b00000000):
			dtc_string = dtc_string + ‘0’
		elif(b_bit3_0 = 0b00000001):
			dtc_string = dtc_string + ‘1’
		elif(b_bit3_0 = 0b00000010):
			dtc_string = dtc_string + ‘2’
		elif(b_bit3_0 = 0b00000011):
			dtc_string = dtc_string + ‘3’
		elif(b_bit3_0 = 0b00000100):
			dtc_string = dtc_string + ‘4’
		elif(b_bit3_0 = 0b00000101):
			dtc_string = dtc_string + ‘5’
		elif(b_bit3_0 = 0b00000110):
			dtc_string = dtc_string + ‘6’
		elif(b_bit3_0 = 0b00000111):
			dtc_string = dtc_string + ‘7’
		elif(b_bit3_0 = 0b00001000):
			dtc_string = dtc_string + ‘8’
		elif(b_bit3_0 = 0b00001001):
			dtc_string = dtc_string + ‘9’
        elif(b_bit3_0 = 0b00001010):
            dtc_string = dtc_string + A’
		elif(b_bit3_0 = 0b00001011):
			dtc_string = dtc_string + ‘B’
		elif(b_bit3_0 = 0b00001100):
			dtc_string = dtc_string + ‘C’	
		elif(b_bit3_0 = 0b00001101):
			dtc_string = dtc_string + ‘D’
		elif(b_bit3_0 = 0b00001110):
			dtc_string = dtc_string + ‘E’
		elif(b_bit3_0 = 0b00001111):
			dtc_string = dtc_string + ‘F’		

return dtc_string;

def hex_to_bin(hex):
    return ''.join('{:08b}'.format(int(x, 16)) for x in _chunks(hex, 2));
