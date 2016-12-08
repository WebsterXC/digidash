import socketrun
import blue
import automath

def main():
	b = blue.Blue()
	b.connect()

	res = send_recv("atz")
	res = send_recv("ate0")

	for i in range(0, 100):
		res = send_recv("010C")
		r = res.split()

		automath.eng_rpm_conv(r[2], r[3])

	b.disconnect()
