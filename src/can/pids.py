#################################################
#   ======    =====    ======   =====
#   ||	 \\     |     //	  |
#   ||    \\    |    // 	  |
#   ||    //    |    ||  =====	  |   --------
#   ||   //     |    \\     //	  |
#   ======    =====   ======    =====
##################################################

# [Summary]: This file represents the standard vehicle PID codes as defined by
# the OBD-II standard. PIDs are represented as strings, because the underlying
# bluetooth communication sends/receives ASCII characters. In addition, macros
# for OBD-II mode and ELM327 mode are offered as well.

##### General #####
SPEED            = "0x0D"
RTES             = "0x1F"     # Runtime since engine start
ENVIR_PRESS      = "0x33"     # Ambient air barometric pressure (kPa, absolute)
ENVIR_TEMP       = "0x46"     # Ambient air temperature (deg. Celcius)

##### Engine #####
ENG_LOAD         = "0x04"     # Engine load (%)
ABS_LOAD         = "0x43"     # Absolute engine load value (0% <= x < 25700%)
ENG_COOLTEMP     = "0x05"     # Engine coolant temperature(deg. Celcius)
ENG_RPM          = "0x0C"     # Engine RPM (rpm)
ENG_TORQUE_DMD   = "0x61"     # Driver's demand engine torque (-125% <= x <= 125%)
ENG_TORQUE_ACT   = "0x62"     # Actual engine torque being delivered
ENG_TORQUE_REF   = "0x63"     # Engine reference torque (Newton/meters)
ENG_TIME         = "0x7F"     # Engine run time

##### Airflow #####
INTAKE_PRESS     = "0x0B"     # Intake air manifold pressure (kPa, absolute)
INTAKE_TEMP      = "0x0F"     # Intake air temperature(deg. Celcius)
INTAKE_MAF       = "0x10"     # Mass Air Flow sensor flow rate (g/s)
EVAP_PRESS       = "0x32"     # Evaporative system vapor pressure (Pa)
EVAP_CMDED       = "0x2E"     # Commanded evap purge (%)
EXHST_PRESS      = "0x73"     # Exhaust pressure

##### Oil #####
OIL_TEMP         = "0x5C"     # Engine oil temperature (deg. Celcius)

##### Fuel #####
FUEL_PRESS       = "0x0A"     # Fuel system pressure (kPa, gauge)
FUEL_PRESS_ABS   = "0x56"     # Fuel system pressure (kPa, absolute)
FUEL_ADVAN       = "0x0E"     # Fuel timing advance/retard (degrees before TDC)
FUEL_TIMING      = "0x5D"     # Fuel injection timing (relative crankshaft degrees)
FUEL_LEVEL       = "0x2F"     # Fuel tank remaining (%)
FUEL_CMDED       = "0x44"     # Fuel/Air commanded equivalence ratio (O <= x < 2)
FUEL_RATE        = "0x5E"     # Fuel consumption (L/h)


##### Fuel Banks #####

# Fuel banks are a calculated percentage of sensed air-fuel ratio. The ideal
# scenario is a value of 0:
    # -100 <= x < 0 denotes fuel that is too rich
    # 0 < x <= 99.2 denotes fuel that is too lean
FUEL_BANK_SHORT1 = "0x06"     # Short term fuel bank 1 (%)
FUEL_BANK_SHORT2 = "0x08"     # Short term fuel bank 2
FUEL_BANK_LONG1  = "0x07"     # Long term fuel bank 1
FUEL_BANK_LONG2  = "0x09"     # Long term fuel bank 2

##### Catalytic Converter Sensors #####

## Cat Sensors are in front of the catalytic converter. ##
CAT_TEMP_B1S1    = "0x3C"     # Catalyst Temperature, Bank 1 Sensor 1
CAT_TEMP_B2S1    = "0x3D"
CAT_TEMP_B1S2    = "0x3E"
CAT_TEMP_B2S2    = "0x3F"

##### Oxygen Sensors #####
## O2 sensors are behind the catalytic converter. ##

# Directly read sensor voltages from 0 <= x <= 1.275
OXSNS_COUNT      = "0x13"     # Number of oxygen sensors equipped.
OXSNS_V1         = "0x14"     # Oxygen sensor #1 (voltage)
OXSNS_V2         = "0x15"     
OXSNS_V3         = "0x16"
OXSNS_V4         = "0x17"
OXSNS_V5         = "0x18"
OXSNS_V6         = "0x19"
OXSNS_V7         = "0x1A"
OXSNS_V8         = "0x1B"

OXSNS_FA1        = "0x34"     # Oxygen sensor #1 F/A ratio (0 <= x < 2)
OXSNS_FA2        = "0x35"
OXSNS_FA3        = "0x36"
OXSNS_FA4        = "0x37"
OXSNS_FA5        = "0x38"
OXSNS_FA6        = "0x39"
OXSNS_FA7        = "0x3A"
OXSNS_FA8        = "0x3B"

##### TURBO #####
TURBO_PRESS      = "0x6F"     # Turbocharger compressor inlet pressure
TURBO_RPM        = "0x74"     # Turbocharger impeller RPM
TURBO_TEMP       = "0x75"     # Turbocharger temperature
INTCOOL_TEMP     = "0x77"     # Intercooler temperature

##### Misc #####
THROTTLE_REQ     = "0x11"     # Throttle Position (%)
THROTTLE_REL     = "0x45"     # Relative Throttle Position (%)
ACCEL_REQ        = "0x5A"     # Relative Accellerator Position (%)

##### CAN Modes #####
MODE_ELM	 = "0x00"
MODE_REALTIME	 = "0x01"
MODE_FREEZE	 = "0x02"
MODE_DTC	 = "0x03"
MODE_DTC_CLR	 = "0x04"
