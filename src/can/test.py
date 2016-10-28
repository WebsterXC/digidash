import canbus
import automath
import pids

c = canbus.canbus()

for i in range (0, 20):
#while 1:
	result = canbus.send_pid(pids.ENG_RPM)
	

	data = result.split()
	
	if i > 3:
		a = int(data[2], 16)
		b = int(data[3], 16)
		print( automath.eng_rpm_conv(a, b) )
	
