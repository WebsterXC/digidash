# File defines individual methods for converting raw CAN bus data to usable values.

# Naming convention is all lowercase, <parameter name>_conv(args)
# Ordering of methods is the same ordering of PIDs in pids.py

# Sources:
#   - "OBD-II PIDs" Wikipedia Page


##### Helpers #####

# Function takes data in 2's complement and returns it's decimal equivalent.
def twos_to_decimal(number):
    return -1   #Unimplemented

##### General #####

def speed_conv(data):
    return data

def rtes_conv(byteA, byteB):
    return (256*byteA) + byteB

def envir_press_conv(data):
    return data

def envir_temp_conv(data):
    return data


##### Engine #####

def eng_load_conv(data):
    return data / 2.55

def abs_load_conv(byteA, byteB):
    return ((256*byteA) + byteB) / 2.55

def eng_cooltemp_conv(data):
    return data - 40

def eng_rpm_conv(byteA, byteB):
    return ((256*byteA) + byteB) / 4

def eng_torque_dmd_conv(data):
    return data - 125

def eng_torque_act_conv(data):
    return data - 125
    
def eng_torque_ref_conv(byteA, byteB):
    return (256 * byteA) + byteB

def eng_time_conv(data):
    return 0        # No conversion formula in reference.


##### Airflow #####

def intake_press_conv(data):
    return data

def intake_temp_conv(data):
    return data - 40

def intake_maf_conv(byteA, byteB):
    return ((256*byteA) + byteB) / 100

def evap_press_conv(byteA, byteB):
    # Data is 2's-complement signed.
    dataA = twos_to_decimal(byteA)
    dataB = twos_to_decimal(byteB)
    return ((256*dataA) + dataB) / 4

def evap_cmded_conv(data):
    return data / 2.55

def exhst_press_conv(data):
    return 0        # No conversion formula in referece.


##### Oil #####

def oil_temp_conv(data):
    return data - 40


##### Fuel #####

def fuel_press_conv(data):
    return data*3

def fuel_press_abs_conv(byteA, byteB):
    return ((256*byteA) + byteB) * 10

def fuel_advan_conv(data):
    return (data/2) - 64 

def fuel_timing_conv(byteA, byteB):
    return ( ((256*byteA) + byteB) / 128) - 210 

def fuel_level_conv(data):
    return data / 2.55

def fuel_cmded_conv(data):
    return (2/65536) * ((256*byteA) + byte B)

def fuel_rate_conv(byteA, byteB):
    return ( (256*byteA) + byteB) / 20


##### Fuel Banks #####

def fuel_bank_conv(data):
    return (data/1.28) - 100


##### Cat Sensors #####

def cat_temp_conv(byteA, byteB):
    return ( ((256*byteA) + byteB) / 10) - 40


##### Oxygen Sensors #####

def oxsns_volts_conv(data):
    return data / 200

def oxsns_fa_conv(byteA, byteB):
    return ( (2/65536) * ((256*byteA)+byteB))


##### Turbo #####
# Codes are OBD-II standard, but data returned might be proprietary.
# Conversion formulas not specified in reference.

def turbo_press_conv(data):
    return 0

def turbo_rpm_conv(data):
    return 0

def turbo_temp_conv(data):
    return 0

def intcool_temp_conv(data):
    return 0


##### Misc #####

def throttle_req_conv(data):
    return data / 2.55
def throttle_rel_conv(data):
    return data / 2.55
def accel_req_conv(data):
    return data / 2.55
