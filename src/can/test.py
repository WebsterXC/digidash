import dtc

def main():
	# One DTC code (P2468) is set.
	ret = dtc.dtc_scan("SEARCHING... 43 00 24 68")
	print(ret)

	# No DTC codes are set.
	ret = dtc.dtc_scan("SEARCHING... 43 00")
	print(ret)

if __name__ == "__main__":
	main()
