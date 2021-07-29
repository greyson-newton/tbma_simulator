import matplotlib.pyplot as plt
from math import exp
from scipy.stats import norm

class Plotter:
	def __init__(self, xInit, xFinal, momentum):

		self.x = range(xInit, xFinal)
		print(type(momentum))
		self.Y = [momentum*exp(-0.5*_) for _ in self.x]
		self.size = len(self.x)
		self.error = norm.rvs(0, scale=0.0001, size=self.size)
		self.simulated_data = [max(0, y+e) for (y,e) in zip(self.Y[:self.size],self.error)]		

		#print(self.simulated_data)

		self.fig = plt.figure(figsize = (14,10))

		self.sub1 = fig.add_subplot(2,1,2)
		self.sub1.set_title('Visual of Alignment')
		self.sub1.margins(0.05)           # Default margin is 0.05, value 0 means fit
		self.sub1.set_xlim([0, 75])
		self.sub1.set_ylim([-150, 150])

		self.sub2 = fig.add_subplot(2,2,1)
		self.sub2.set_title('Alignment Step')

		self.sub3 = fig.add_subplot(2,2,2)
		self.sub3.set_title('Residual')
		self.fig.suptitle('Fastest Job')
	def returnStepSize(self, index):
		return self.Y[index]
	def returnStepSizes(self):
		return self.Y
	def updateEndpoints(self, actualEndpoints, designEndpoints):
		legend = sub1.legend()
		self.actualEndpoints = actualEndpoints
		self.designEndpoints = designEndpointsOne
		self.designPlotOne = self.sub1.plot(self.designEndpointsOne[0],self.designEndpointsOne[1], color='blue', label="design Chamber Postition")
		self.actualPlotOne = self.sub1.plot(self.actualEndpointsOne[0],self.actualEndpointsOne[1], color='green', label="actual Chamber Postition")
		
		self.fig.plause(0.0001)
		for x in self.muonPath:
			x.remove()
		for i in self.trackPath:
			i.remove()
	def updateMuonPath(self, muonTrackOne, muonPathOne):
		self.muonTrack = muonTrackOne
		self.muonPath = muonPathOne
		self.sub1.plot(self.muonTrack[0], self.muonTrack[1], color='orange', label="track")
		self.sub1.plot(self.muonPath[0],self.muonPath[1], marker = 'o', color='red', label="actual path")

	def updateSubTwo(self, xCount, yCount, zCount):
		
		self.xPt, self.yPt, self.zPt = [xCount, xCount], [yCount, yCount], [zCount, zCount]
		self.xLine  = [0, self.Y[xCount]]
		self.yLine=[0, self.Y[yCount]]
		self.zLine[0, self.Y[zLine]]
						#axs = plt.subplots(nrows=3, ncols=2, sharex=True, sharey=True, figsize = (10,6), gridspec_kw={'hspace': 0})
		self.sub2.plot(self.x, self.Y, 'b-')
		self.sub2.plot(self.x[:self.size], self.simulated_data, 'r.')
		self.sub2.plot(self.xPt, xLine, 'r.')
		self.sub2.plot(self.yPt, yLine, 'r.')
		self.sub2.plot(self.zPt, zLine, 'r.')


	def updateSubThree(self, yResidual):
		self.residualPlot = self.sub3.hist(self.yResidual)

