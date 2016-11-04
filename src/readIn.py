#Supporting code for Add Gauge 
#reads .csv into dictionary

import csv
import sys

type = {}
values = []

def readIn(csvf):
	count = 0

	with open(csvf, 'rb') as x:
		worddup = csv.reader(x)

		for row in worddup:
			for mow in row:
				values.append(mow)
			

			type[values[count]] = row
			#del values[count]

			count += 4
		
		print type
	return type


def assign(type, userPick):

	gauge = type.get(userPick)
	#print gauge
	
	gaugeType = gauge[0]
	minVal = gauge[1]
	maxVal = gauge[2]
	units = gauge[3]
	print gaugeType
	print minVal
	print maxVal
	print units

	return  
if __name__ == '__main__':
    
    if len(sys.argv) < 3:
        print("Please provide the .CSV as the argument")
        sys.exit

    input_file = sys.argv[1]
    userPick = sys.argv[2]

    
    type = readIn(input_file)
    assign(type, userPick)