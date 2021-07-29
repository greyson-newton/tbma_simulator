import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from math import exp
from scipy.stats import norm

#windows
from win32api import GetSystemMetrics

#mac
# from Quartz import CGDisplayBounds
# from Quartz import CGMainDisplayID


#SMALL_SIZE = 8
#MEDIUM_SIZE = 10
#BIGGER_SIZE = 12

#plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
#plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
#plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
#plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
#plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
#plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
#plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title


class plotter:
	def __init__(self, xInit, xFinal, momentum, nIterations):

		self.z = 0
		self.nIterations = nIterations
		self.momentum = momentum
		plt.style.use('seaborn')
		plt.rc('xtick', labelsize=17)    # fontsize of the tick labels
		plt.rc('ytick', labelsize=17)
		plt.rc('legend', fontsize=20)
		plt.rc('font', size=15)
		plt.rc('axes', labelsize=15)    # fontsize of the x and y labels
		
		self.x = range(xInit, xFinal)
		self.Y = [self.momentum*exp(-0.5*_) for _ in self.x]
		self.size = len(self.x)
		self.error = norm.rvs(0, scale=0.0001, size=self.size)
		self.simulated_data = [max(0, y+e) for (y,e) in zip(self.Y[:self.size],self.error)]		

		#print(self.simulated_data)

		#windows
		self.width = GetSystemMetrics(0)
		self.height = GetSystemMetrics(1)

		#mac
		# mainMonitor = CGDisplayBounds(CGMainDisplayID())
		# self.width = mainMonitor.size.width
		# self.height = mainMonitor.size.height

		self.fig = plt.figure(figsize = (self.width,self.height))
		self.sub1 = self.fig.add_subplot(2,1,2)
		self.sub1.set_title('Visual', fontsize=25)
		self.sub1.margins(0.05)           # Default margin is 0.05, value 0 means fit
		self.sub1.set_xlim([0, 75])
		self.sub1.set_ylim([-150, 150])

		self.sub2 = self.fig.add_subplot(2,2,1)
		self.sub2.set_title('Alignment Step', fontsize=25)

		self.sub3 = self.fig.add_subplot(2,2,2)
		self.sub3.set_title('Residual', fontsize=25)
		self.sub3.set_xlim([-3, 3])
		self.sub3.set_ylim([0, 3000])
		self.fig.suptitle('Fastest Job', fontsize=35)
		#sub1legend = self.sub1.legend(loc='lower left', bbox_to_anchor=(0.5, -0.05), shadow=True)
		#sub2legend = self.sub2.legend(loc='lower left', bbox_to_anchor=(0.5, -0.05), shadow=True
		np.random.seed(42)
		data = np.random.rand(4,4)
		cMap = mpl.cm.get_cmap('viridis', 20)
		heat = self.sub3.pcolor(data, cmap=cMap)
		cbar = plt.colorbar(heat)
		cbar.ax.get_yaxis().set_ticks([])
		for j, lab in enumerate(['$1-5$','$6-10$','$10-15$','$15-20$']):
			cbar.ax.text(2, (2 * j + 1) / 8.0, lab, ha='center', va='center')
		cbar.ax.get_yaxis().labelpad = 90
		cbar.ax.set_ylabel('Iterational Residual', rotation=270, fontsize = 25)

		self.Xann = self.sub2.annotate('X Step', xy = (0, 0), xytext=(0, .25))
		self.Yann = self.sub2.annotate('Y Step', xy = (0, 0), xytext=(0, .25))
		self.Zann = self.sub2.annotate('Z Step', xy = (0, 0), xytext=(0, .25))


	def returnStepSize(self, index):
		return self.Y[index]
	def returnStepSizes(self):
		return self.Y
	def show(self):
		plt.show()
	def updateEndpoints(self, actualEndpoints, designEndpoints):
		self.sub1.margins(0.05)           # Default margin is 0.05, value 0 means fit
		self.sub1.set_xlim([0, 75])
		self.sub1.set_ylim([-150, 150])
		self.sub1.set_ylabel('Local y', fontsize=25)
		self.sub1.set_xlabel('Local x', fontsize=25)
		self.actualEndpoints = actualEndpoints
		self.designEndpoints = designEndpoints
		self.designPlot = self.sub1.plot(self.designEndpoints[0],self.designEndpoints[1], color='blue', label="design Chamber Postition")
		self.actualPlot = self.sub1.plot(self.actualEndpoints[0],self.actualEndpoints[1], color='green', label="actual Chamber Postition")
		
	def updateMuonPath(self, muonTrackOne, muonPathOne):
		self.sub1.legend()
		self.muonTrack = muonTrackOne
		self.muonPath = muonPathOne
		self.trackPlot = self.sub1.plot(self.muonTrack[0], self.muonTrack[1], color='orange', label="track")
		self.muonPlot = self.sub1.plot(self.muonPath[0],self.muonPath[1], color='red', label="actual path")

		plt.pause(0.0001)
	def updateLinePlots(self, xCount, yCount, zCount):
		self.sub2.set_ylim([0,(self.momentum)])
		self.sub2.set_xlim([0,15])
		self.sub2.set_xlabel('Step Number', fontsize=25)
		self.sub2.set_ylabel('Step Magnitude', fontsize=25)
		self.xPt, self.yPt, self.zPt = [xCount, xCount], [yCount, yCount], [zCount, zCount]

		if(xCount<=7):
			self.xLine  = [0, self.Y[xCount]]
		if(yCount<=7):
			self.yLine=[0, self.Y[yCount]]
		if(zCount<=7):
			self.zLine = [0, self.Y[zCount]]

		if(xCount==7):
			self.yaxa = xCount
		if(yCount==7):
			self.yaya = yCount
		if(zCount==7):
			self.yaza = zCount

		if(xCount>7):
			self.xLine  = [0, self.Y[self.yaxa]]
		if(yCount>7):
			self.yLine=[0, self.Y[self.yaya]]
		if(zCount>7):
			self.zLine = [0, self.Y[self.yaza]]

						#axs = plt.subplots(nrows=3, ncols=2, sharex=True, sharey=True, figsize = (10,6), gridspec_kw={'hspace': 0})
		self.sub2.plot(self.x, self.Y, color = 'black')
		self.datapointPlot = self.sub2.plot(self.x[:self.size], self.simulated_data, 'r.')
		self.xPlot = self.sub2.plot(self.xPt, self.xLine, color='blue', lw=2, label = 'x iteration')
		self.yPlot = self.sub2.plot(self.yPt, self.yLine, color='red', lw=2, label = 'y iteration')
		self.zPlot = self.sub2.plot(self.zPt, self.zLine, color='green', lw=2, label = 'phi iteration')


		self.Xann.set_position((xCount, .25))
		self.Yann.set_position((yCount, .25))
		self.Zann.set_position((zCount, .25))

	def updateResidualPlot(self, yResidual):

		colors = plt.cm.viridis(np.linspace(0, 1, 15))
		self.residualPlot = self.sub3.hist(yResidual, color=colors[self.z])
		self.z = self.z + 1


	def resetMuonPaths(self):
		
		for x in self.muonPlot:
			x.remove()
		for x in self.trackPlot:
			x.remove()
		self.sub1.legend()
	def resetEndpoints(self):
		self.sub1.legend()
		for x in self.designPlot:
			x.remove()
		for x in self.actualPlot:
			x.remove()
	def resetLinePlot(self):
		self.sub2.legend()
		for x in self.xPlot:
			x.remove()
		for x in self.yPlot:
			x.remove()
		for x in self.zPlot:
			x.remove()

		#self.sub2.clear()
		#self.sub2.legend()