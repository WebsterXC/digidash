# File defines individual methods for converting raw CAN bus data to usable values. #

# Modifications to this file should follow the naming and order parameters of pids.py:
    # Naming convention is all lowercase, <parameter name>_conv(args)
    # Ordering of methods is the same ordering of PIDs in pids.py

# Sources:
#   - "OBD-II PIDs" Wikipedia Page

import pids
import math


# Function provides a decision-making process when the data is automatically retreived. Requires input pid and raw ELM data.
def convert(pid, raw):
        SingleByte = {pids.ACCEL_REQ : accell_req_conv, pids.THROTTLE_REL : throttle_rel_conv, pids.FUEL_CMDED : fuel_cmded_conv,              \
                      pids.FUEL_PRESS : fuel_press_conv, pids.EXHST_PRESS : exhst_press_conv, pids.EVAP_CMDED : evap_cmded_conv,               \
                      pids.ENG_TIME : eng_time_conv, pids.ENG_TORQUE_ACT : eng_torque_act_conv, pids.ENG_TORQUE_DMD : eng_torque_dmd_conv,     \
                      pids.ENG_COOLTEMP : eng_cooltemp_conv, pids.ENG_LOAD : eng_load_conv, pids.ENVIR_TEMP : envir_temp_conv,                 \
                      pids.ENVIR_PRESS : envir_press_conv, pids.SPEED : speed_conv, pids.INTAKE_TEMP : intake_temp_conv,                       \
                      pids.INTAKE_PRESS : intake_press_conv, pids.OIL_TEMP : oil_temp_conv, pids.FUEL_ADVAN : fuel_advan_conv,                 \
                      pids.FUEL_LEVEL : fuel_level_conv, pids.THROTTLE_REQ : throttle_req_conv}
	
        DoubleByte = {pids.FUEL_PRESS_ABS : fuel_press_abs_conv, pids.EVAP_PRESS : evap_press_conv, pids.ENG_TORQUE_REF : eng_torque_ref_conv, \
                      pids.ABS_LOAD : abs_load_conv, pids.RTES : rtes_conv, pids.ENG_RPM : eng_rpm_conv,                                       \
                      pids.INTAKE_MAF : intake_maf_conv, pids.FUEL_TIMING : fuel_timing_conv, pids.FUEL_RATE : fuel_rate_conv}

	data = raw.split()
	
	a = 0
	b = 0
	#print(data)	
	if len(data) > 3:
		a = int(data[2], 16)
		b = int(data[3], 16)

	if pid in SingleByte:               # Single variable conversions
		return SingleByte[pid](a)
	elif pid in DoubleByte:             # Two variable conversions
		return DoubleByte[pid](a,b)
        
        # Fuel Bank PIDs
        fuel_pids = [pids.FUEL_BANK_SHORT1, pids.FUEL_BANK_SHORT2, pids.FUEL_BANK_LONG1, pids.FUEL_BANK_LONG2]
        if pid in fuel_pids:
            return fuel_bank_conv(a)

        # Cat Sensor PIDs
        cat_pids = [pids.CAT_TEMP_B1S1, pids.CAT_TEMP_B2S1, pids.CAT_TEMP_B1S2, pids.CAT_TEMP_B2S2]
        if pid in cat_pids:
            return cat_temp_conv(a, b)

        # O2 Sensor PIDs
        oxy_volts = [pids.OXSNS_COUNT, pids.OXSNS_V1, pids.OXSNS_V2, pids.OXSNS_V3, pids.OXSNS_V4, pids.OXSNS_V5, pids.OXSNS_V6, pids.OXSNS_V7, pids.OXSNS_V8]
        if pid in oxy_pids:
            return oxsns_volts_conv(a)
                    
        oxy_fuelair = [pids.OXSNS_FA1, pids.OXSNS_FA2, pids.OXSNS_FA3, pids.OXSNS_FA4, pids.OXSNS_FA5, pids.OXSNS_FA6, pids.OXSNS_FA7, pids.OXSNS_FA8]
        if pid in oxy_fuelair:
            return oxsns_fa_conv(a, b)

	else:
                print("Automath conversion error: PID is not defined.")
		print(pid)

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

def fuel_cmded_conv(byteA, byteB):
    return (2/65536) * ((256*byteA) + byteB)

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

## Unit Conversions to Imperial ##

# kPa to PSI
def units_psi(value):
	return value * 0.14503773773

# km/h to Mi/h
def units_kmh(value):
	return value / 1.609344

# Celcius to fahrenheit
def units_celcius(value):
	return (value * 1.8) + 32

## Data processing calculations for post-conversion data ##

# Estimate horsepower from torque and rpm
def horsepower_calc(torque, rpm):
	return (torque * rpm) / 5252.0

# Estimate horsepower from a quarter mile pull
def quartermile_calc(weight, speed):
	return  ((speed * speed * speed) / 12812904.0) * weight

# Dyno correction factor for naturally aspirated engines. Generates a correction factor
# based on current air temperature and pressure.
def dynocorrect_calc(press, temp):
	return 1.180 * ( (990.0/press) * sqrt((temp+273)/298.0) ) - 0.18

def powerweight_calc(torque, rpm, weight):
	return float(horsepower_calc(torque, rpm)) / float(weight)

