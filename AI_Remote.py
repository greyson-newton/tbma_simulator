import numpy as np
import os, math
from datetime import datetime
from GraphicMultpleScattering import *
from multpleScattering import *
from logWriter import *
from dataManager import *
import pandas as pd
class AI_Remote:
	def __init__(self):
		self.date = datetime.now().strftime("%Y%m%d-%H%M%S")
		self.txtFilename = "log_" + self.date + "_.txt"
		self.csvFilename = "log_" + self.date + "_.csv"
		self.log = logWriter(self.txtFilename)
		self.count = 0
		self.nJobs = 0
		self.nIterations = []
		self.nMomenta = []
		self.SortByTime = False
		self.SortByIterations = True

	def start(self,sim_data):
		#self.progressWindow = progressWindow()
	
		self.x, self.y, self.z, self.theta, self.eta, self.phi, self.d_x, self.d_y, self.d_z,self.d_theta, self.d_eta, self.d_phi, self.cham_w, self.cham_h, self.Accuracy, self.momentum = AI_DATA[0], AI_DATA[1], AI_DATA[2], int(AI_DATA[3]), int(AI_DATA[4]), int(AI_DATA[5]), int(AI_DATA[6]), int(AI_DATA[7]), int(AI_DATA[8])

		graphic=True

		if graphic:
			program = GraphicMultpleScattering(self.z,self.y,self.phi, self.dz, self.dy, self.dp, self.Length, self.Accuracy, self.momentum)

		self.count+=1
		print("\n-------------------------------------------------------------")
		print("Job Number: ", self.count, " |",  " Time: ", program.returnTime(), "|", "nIterations: ", program.returnNumberOfIterations())
		print("--------------------------------------------------------------\n")
		self.times.append(program.returnTime())
		self.DzPos.append(DzValue) 
		self.DyPos.append(DyValue) 
		self.DphiPos.append(DpValue)
		self.zPos.append(self.z)
		self.yPos.append(self.y)
		self.phiPos.append(self.phi)
		self.nIterations.append(program.returnNumberOfIterations())
		self.nMomenta.append(program.returnMomentum())

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