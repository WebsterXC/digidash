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
					#print(mow)

				types[values[count]] = row
				#del values[count]

				count += 5
		
			#print(types)
		return types


	def assign(self, types, userPick):

		gauge = types.get(userPick)
		#print gauge
	
		gaugeType = gauge[0]
		minVal = gauge[1]
		maxVal = gauge[2]
		units = gauge[3]
#		print gaugeType
#		print minVal
#		print maxVal
#		print units

		return  
	#if __name__ == '__main__':
		
		#if len(sys.argv) < 3:
		 #   print("Please provide the .CSV as the argument")
		  #  sys.exit

		#input_file = sys.argv[1]
		#userPick = sys.argv[2]

		
		#type = readIn(input_file)
		#assign(type, userPick)
