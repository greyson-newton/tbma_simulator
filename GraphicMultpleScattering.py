
#tkinker GUI
#		https://www.cs.uct.ac.za/mit_notes/python/Introduction_to_GUI_Programming.html
#simulating environments - simpy documentation
#		https://realpython.com/simpy-simulating-with-python/#what-simulation-is
#PyQt5 GUI


from numba import *
import math, random, time
from geometry import *
from constants import *
from iterateMuon import iterateMuon
from circleIntersectLine import circleIntersectLine
from propagateMuon import propagateMuon
from chamber import *
import numpy as np
from plotter import *
from expDecay import *
from dataManager import *
random.seed(1.0)

class tbma_dt_simulation ():
	def __init__(self):
		self.nIterations=0
		self.aligned = False
		self.Zinit, self.Zfinal = 0, 50
		self.expFit = expDecay(self.Zinit, self.Zfinal, self.momentum)
		self.stepSizes = self.expFit.returnStepSizes()
		
		self.chamber = chamber(1, self.Length, self.Z, self.Y, self.Phi, self.Z+self.Dz, self.Y+self.Dy, self.Phi+self.dPhi, self.Accuracy, self.stepSizes)
		
		dataManager(self.Zinit, self.Zfinal, float(self.momentum), self.nIterations)
		self.stepSizes = self.plotter.returnStepSizes()

		for i in range(400):
			if self.chamber.isDone(): #and self.chamber2.isDone() and self.chamber3.isDone()
				break
			self.actualEndpoints = self.chamber.actualEndpoints
			self.designEndpoints = self.chamber.designEndpoints
			self.plotter.updateEndpoints(self.actualEndpoints, self.designEndpoints)
			self.plotter.updateResidualPlot(self.chamber.returnResidual())
			self.plotter.updateLinePlots(self.chamber.countZ, self.chamber.countY, self.chamber.countP)
			
			shootMuons(self.chamber, self.plotter)

			self.chamber.align()
			self.chamber.resetData()

			self.plotter.resetEndpoints()
			self.plotter.resetLinePlot()

	def returnTime(self):
		return self.time

def shootMuons(chamber, plotter):
	for i in range(nEvents):

		if i%1000==0: i*1.0/nEvents

		#set up inital state of muon
		angleInitial = 1
		speedInitial = 1000
		muon = Muon()
		angleInitial = random.random()-.5

		charge = random.random()
		if charge > .5: charge = 1
		else: charge = -1


		xInitial = 0
		yInitial = 0
		muonPath = []
		muonTrack = []
		#create muon track
		#if verbose > 5: print("start  angle {} speed {} charge {} x {} y {}".format( angleInitial, speedInitial, charge, xInitial, yInitial))
		dataManager.update_muon_data(propagateMuon(angleInitial, speedInitial, charge, xInitial, yInitial))
		self.chamber.getResiduals()
		if i%10000==0:
			dataManager.update_muon_plot()


		# note the y and x axis are not to scale, meaning things are stretched. A tilted chamber will look shorter
		
			#plt.clf()
			#trackPathsOne = sub1.plot(muonTrackOne[0],muonTrackOne[1], color='orange', label="track")
			#muonPathsOne = sub1.plot(muonPathOne[0],muonPathOne[1], marker = 'o', color='red', label="actual path")
			
			#trackPathsTwo = sub2.plot(muonTrackTwo[0],muonTrackTwo[1], color='orange', label="track")
			#muonPathsTwo = sub2.plot(muonPathTwo[0],muonPathTwo[1], marker = 'o', color='red', label="actual path")

			#trackPathsThree = sub3.plot(muonTrackThree[0],muonTrackThree[1], color='orange', label="track")
			#muonPathsThree = sub3.plot(muonPathThree[0],muonPathThree[1], marker = 'o', color='red', label="actual path")
		
			
