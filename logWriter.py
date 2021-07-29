import csv, os
class logWriter:
	def __init__(self, textName):
		self.textName = textName

		self.log = open(self.textName, "w+")

	def writeCSV(self, csvData, csvName):
		example = csv.writer(open(csvName, 'w'))
		example.writerows(csvData)


	def writeTXT(self, minTimeIndex, minTimeCoordinates, nJobs):
		self.minTimeIndex = minTimeIndex
		if nJobs == 3 or nJobs > 3:
			print("# 1: \n", self.minTimeIndex[0], "st Job",  file = self.log)
			print("Design Position: " ,str(minTimeCoordinates[0]) , ",", str(minTimeCoordinates[1]), "," , str(minTimeCoordinates[2]) , 
				"\nActual Position: ", str(minTimeCoordinates[3]) , "," , str(minTimeCoordinates[4]) , ",", str(minTimeCoordinates[5]), file=self.log)
			print("Accuracy: ", str(minTimeCoordinates[18]), "Length: ", str(minTimeCoordinates[19]), file=self.log)

			print("# 2: \n", self.minTimeIndex[1], "nd Job",  file = self.log)
			print("Design Position: " ,str(minTimeCoordinates[6]) , ",", str(minTimeCoordinates[7]), "," , str(minTimeCoordinates[8]) , 
				"\nActual Position: ", str(minTimeCoordinates[9]) , "," , str(minTimeCoordinates[10]) , ",", str(minTimeCoordinates[11]), file=self.log)
			print("Accuracy: ", str(minTimeCoordinates[18]), "Length: ", str(minTimeCoordinates[19]), file=self.log)

			print("# 3: \n", self.minTimeIndex[2], "rd Job",  file = self.log)
			print("Design Position: " ,str(minTimeCoordinates[12]) , ",", str(minTimeCoordinates[13]), "," , str(minTimeCoordinates[14]) , 
				"\nActual Position: ", str(minTimeCoordinates[15]) , "," , str(minTimeCoordinates[16]) , ",", str(minTimeCoordinates[17]), file=self.log)
			print("Accuracy: ", str(minTimeCoordinates[18]), "Length: ", str(minTimeCoordinates[19]) , file=self.log)
		elif nJobs == 2:
			print("# 1: \n", self.minTimeIndex[0], "st Job",  file = self.log)
			print("Design Position: " ,str(minTimeCoordinates[0]) , ",", str(minTimeCoordinates[1]), "," , str(minTimeCoordinates[2]) , 
				"\nActual Position: ", str(minTimeCoordinates[3]) , "," , str(minTimeCoordinates[4]) , ",", str(minTimeCoordinates[5]), file=self.log)
			print("Accuracy: ", str(minTimeCoordinates[12]), "Length: ", str(minTimeCoordinates[13]), file=self.log)

			print("# 2: \n", self.minTimeIndex[1], "nd Job",  file = self.log)
			print("Design Position: " ,str(minTimeCoordinates[6]) , ",", str(minTimeCoordinates[7]), "," , str(minTimeCoordinates[8]) , 
				"\nActual Position: ", str(minTimeCoordinates[9]) , "," , str(minTimeCoordinates[10]) , ",", str(minTimeCoordinates[11]), file=self.log)
			print("Accuracy: ", str(minTimeCoordinates[12]), "Length: ", str(minTimeCoordinates[13]), file=self.log)
		elif nJobs == 1:
			print("# 1: \n", self.minTimeIndex[0], "st Job",  file = self.log)
			print("Design Position: " ,str(minTimeCoordinates[0]) , ",", str(minTimeCoordinates[1]), "," , str(minTimeCoordinates[2]) , 
				"\nActual Position: ", str(minTimeCoordinates[3]) , "," , str(minTimeCoordinates[4]) , ",", str(minTimeCoordinates[5]), file=self.log)
			print("Accuracy: ", str(minTimeCoordinates[6]), "Length: ", str(minTimeCoordinates[7]), file=self.log)
		else:
			print('no jobs', self.log)
			print('no jobs')
			#except:
			#	print("couldnt write log")