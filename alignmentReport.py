import numpy as np
import os, math
from datetime import datetime
from GraphicMultpleScattering import *
from multpleScattering import *
import csv, os
from logWriter import *
from dataManager import *
import pandas as pd


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
        
class alignmentReport:
	def __init__(self):

		self.date = datetime.now().strftime("%Y%m%d-%H%M%S")
		self.txtFilename = "log_" + self.date + "_.txt"
		self.csvFilename = "log_" + self.date + "_.csv"
        # add sorting option
		self.log = logWriter(self.txtFilename)

		self.nIterations = []
		self.nMomenta = []
		self.SortByTime = False
		self.SortByIterations = True

	def report(self):
        #printing data
        if self.SortByTime:		
            rankedTimes = sorted(self.times)
            rankedIndexes = []
            for i in range(len(rankedTimes)):
                rankedIndexes.append(rankedTimes.index(self.times[i]))
            rankedIndices = sorted(rankedIndexes)
            parameters = ["time_rank", "design_position", "actual_position" , "time_elapsed(seconds)", "momentum", "# of iterations","job_number"] 
            csvData = []
            csvData.append(parameters)
            for i in rankedIndices:
                design_position = [self.zPos[rankedIndices[i]], self.yPos[rankedIndices[i]], math.degrees(self.phiPos[rankedIndices[i]])]
                actual_position = [self.zPos[rankedIndices[i]] + self.DzPos[rankedIndices[i]], self.yPos[rankedIndices[i]] + self.DyPos[rankedIndices[i]], math.degrees(self.phiPos[rankedIndices[i]] + self.DphiPos[rankedIndices[i]])]
                momemtumString = str(self.momentum) + "/" + str(self.nMomenta[rankedIndices[i]])
                appendData = [rankedIndices[i] , design_position, actual_position, self.times[rankedIndices[i]], momemtumString, self.nIterations[rankedIndices[i]], rankedIndexes[i]]
                
                csvData.append(appendData)

            self.log.writeCSV(csvData, self.csvFilename)
        if self.SortByIterations:
            rankedIterations = sorted(self.nIterations)
            rankedIndexes = []
            for i in range(len(rankedIterations)):
                rankedIndexes.append(rankedIterations.index(self.nIterations[i]))
            rankedIndices = sorted(rankedIndexes)
            parameters  = ["iteration_rank", "design_position", "actual_position" , "time_elapsed(seconds)", "momentum", "# of iterations","job_number"]
            csvData = []
            csvData.append(parameters)
            for i in rankedIndices:
                design_position = [self.zPos[rankedIndices[i]], self.yPos[rankedIndices[i]], math.degrees(self.phiPos[rankedIndices[i]])]
                actual_position = [self.zPos[rankedIndices[i]] + self.DzPos[rankedIndices[i]], self.yPos[rankedIndices[i]] + self.DyPos[rankedIndices[i]], math.degrees(self.phiPos[rankedIndices[i]] + self.DphiPos[rankedIndices[i]])]
                momemtumString = str(self.momentum) + "/" + str(self.nMomenta[rankedIndices[i]])

                appendData = [rankedIndices[i] , design_position, actual_position, self.times[rankedIndices[i]], momemtumString, self.nIterations[rankedIndices[i]], rankedIndexes[i]]
                
                csvData.append(appendData)

            self.log.writeCSV(csvData, self.csvFilename)

	def showPlots(self):

		chamberOneInfo = [self.zPos[self.minTimeOneIndex], self.yPos[self.minTimeOneIndex], self.phiPos[self.minTimeOneIndex], self.DzPos[self.minTimeOneIndex], self.DyPos[self.minTimeOneIndex], self.DphiPos[self.minTimeOneIndex], self.nMomenta[self.minTimeOneIndex]]
		#chamberTwoInfo = [self.zPos[self.minTimeTwoIndex], self.yPos[self.minTimeTwoIndex], self.phiPos[self.minTimeTwoIndex], self.DzPos[self.minTimeTwoIndex], self.DyPos[self.minTimeTwoIndex], self.DphiPos[self.minTimeTwoIndex]]
		#chamberThreeInfo = [self.zPos[self.minTimeThreeIndex], self.yPos[self.minTimeThreeIndex], self.phiPos[self.minTimeThreeIndex], self.DzPos[self.minTimeThreeIndex], self.DyPos[self.minTimeThreeIndex], self.DphiPos[self.minTimeThreeIndex]]

		plot = GraphicMultpleScattering()
		plot.start(chamberOneInfo, self.Length, self.Accuracy, self.nIterations[self.minTimeOneIndex])

	def showSpreadSheet(self):
		os.startfile(self.csvFilename)

	def showLog(self):
		os.startfile(self.txtFilename)

	def setSortingFilter(self, command):
		if command == "time":
			self.SortByTime = True
		if command == "iterations":
			self.SortByIterations = True
		else:
			print("idk")
	def returnJobNumber(self):
		return count

	def returnProgressString(self):
		completionString = (str(self.count) + " jobs complete out of: " + str(self.nJobs))
		return completionString

#print("2 --- time: ", minTimeOne, "x: ", minCoordinatesOne[0], "y: ", minCoordinatesOne[2], "phi: ", minCoordinatesOne[2], file = log)
#print("2 --- time: ", minTimeTwo, "x: ", minCoordinatesTwo[0], "y: ", minCoordinatesTwo[1], "phi: ", minCoordinatesTwo[2], file = log)
#rint("1 --- time: ", minTimeThree, "x: ", minCoordinatesThree[0], "y: ", minCoordinatesThree[1], "phi: ", minCoordinatesThree[2], file = log)