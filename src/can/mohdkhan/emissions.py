
#kkkk
# supports actual DTC if MIL is on

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
    print(“\n”)
       #echoes are already ignored 
    print(“Raw bytes for MIL:”)
    print(buffer)

    data = buffer.split()
    #4 bytes are stored as BITS	
    a = data[2] #mil status
    #if mil is on, car does not pass emission
    b = data[3] #Fuel System, Misfire
    c = data[4] #Test available: EGR System, Oxygen Sensor heater, oxygen sensor, Evap sytem, Heated catalyst, catalyst
    d = data[5] #Test incomplete: EGR System, Oxygen Sensor heater, oxygen sensor, Evap sytem, Heated catalyst, catalyst

   #MIL status and # of DTC codes
   a_copy_mil = hex_to_bin(a)
   print("a_copy_mil: ")
   print(a_copy_mil)
   a_copy_dtc_num = hex_to_bin(a)
   print("a_copy_dtc_num: ")
   print(a_copy_dtc_num)
   
   b_copy_ = hex_to_bin(b)
   
   c_copy_ = hex_to_bin(c)
   
   c_copy_catalyst = c_copy_
       c_copy_catalyst = c_copy_catalyst<<7
       c_copy_catalyst = c_copy_catalyst>>7
               
               c_copy_heatedcatalyst = c_copy_
                   c_copy_heatedcatalyst = c_copy_heatedcatalyst<<6
                       c_copy_heatedcatalyst = c_copy_heatedcatalyst>>6
                           c_copy_heatedcatalyst = c_copy_heatedcatalyst>>1
                               c_copy_heatedcatalyst = c_copy_heatedcatalyst<<1
                                   
                                   c_copy_evap = c_copy_
                                       c_copy_evap = c_copy_evap<<5
                                           c_copy_evap = c_copy_evap>>5
                                               c_copy_evap = c_copy_evap>>2
                                                   c_copy_evap = c_copy_evap<<2
                                                       
                                                       c_copy_oxygensensor = c_copy_
                                                           c_copy_oxygensensor = c_copy_oxygensensor<<2
                                                               c_copy_oxygensensor = c_copy_oxygensensor>>2
                                                                   c_copy_oxygensensor = c_copy_oxygensensor>>5
                                                                       c_copy_oxygensensor = c_copy_oxygensensor<<5
                                                                           
                                                                           c_copy_oxygensensorheater = c_copy_
                                                                               c_copy_oxygensensorheater = c_copy_oxygensensorheater<<1
                                                                                   c_copy_oxygensensorheater = c_copy_oxygensensorheater>>1
                                                                                       c_copy_oxygensensorheater = c_copy_oxygensensorheater>>6
                                                                                           c_copy_oxygensensorheater = c_copy_oxygensensorheater<<6
                                                                                               
                                                                                               c_copy_egr = c_copy_
                                                                                                   c_copy_egr = c_copy_egr>>7
                                                                                                       c_copy_egr = c_copy_egr<<7






  d_copy_ = hex_to_bin(d)

d_copy_catalyst = b_copy_
    d_copy_catalyst = d_copy_catalyst<<7
        d_copy_catalyst = d_copy_catalyst>>7
            
            d_copy_heatedcatalyst = d_copy_
            d_copy_heatedcatalyst = d_copy_heatedcatalyst<<6
            d_copy_heatedcatalyst = d_copy_heatedcatalyst>>6
            d_copy_heatedcatalyst = d_copy_heatedcatalyst>>1
            d_copy_heatedcatalyst = d_copy_heatedcatalyst<<1
                
                d_copy_evap = d_copy_
                    d_copy_evap = d_copy_evap<<5
                        d_copy_evap = d_copy_evap>>5
                            d_copy_evap = d_copy_evap>>2
                                d_copy_evap = d_copy_evap<<2
                                    
                                    d_copy_oxygensensor = d_copy_
                                        d_copy_oxygensensor = d_copy_oxygensensor<<2
                                            d_copy_oxygensensor = d_copy_oxygensensor>>2
                                                d_copy_oxygensensor = d_copy_oxygensensor>>5
                                                    d_copy_oxygensensor = d_copy_oxygensensor<<5
                                                        
                                                        d_copy_oxygensensorheater = d_copy_
                                                            d_copy_oxygensensorheater = d_copy_oxygensensorheater<<1
                                                                d_copy_oxygensensorheater = d_copy_oxygensensorheater>>1
                                                                    d_copy_oxygensensorheater = d_copy_oxygensensorheater>>6
                                                                        d_copy_oxygensensorheater = d_copy_oxygensensorheater<<6
                                                                            
                                                                            d_copy_egr = d_copy_
                                                                                d_copy_egr = d_copy_egr>>7
                                                                                    d_copy_egr = d_copy_egr<<7



port.disconnect();




