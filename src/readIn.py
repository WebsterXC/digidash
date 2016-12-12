#################################################
#   ======    =====    ======   =====
#   ||	 \\     |     //	  |
#   ||    \\    |    // 	  |
#   ||    //    |    ||  =====	  |   --------
#   ||   //     |    \\     //	  |
#   ======    =====   ======    =====
##################################################

# [Summary]: Supporting code for Add Gauge reads .csv into dictionary

import csv

types = {}
values = []

class read:

	def readIn(self, csvf):
		count = 0

		with open(csvf, 'rb') as x:
			worddup = csv.reader(x)
			
			for row in worddup:
				for mow in row:
					values.append(mow)

				types[values[count]] = row

				count += 5
		
		return types


	def assign(self, types, userPick):

		gauge = types.get(userPick)
	
		gaugeType = gauge[0]
		minVal = gauge[1]
		maxVal = gauge[2]
		units = gauge[3]

		return  
