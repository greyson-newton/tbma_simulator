import matplotlib.pyplot as plt
from math import exp
from scipy.stats import norm

class expDecay:
	def __init__(self, xInit, xFinal, momentum):
		self.momentum = int(momentum)
		self.x = range(xInit, xFinal)
		self.Y = [self.momentum*exp(-0.5*_) for _ in self.x]
		self.size = len(self.x)
		self.error = norm.rvs(0, scale=0.0001, size=self.size)
		self.simulated_data = [max(0, y+e) for (y,e) in zip(self.Y[:self.size],self.error)]

		#print(self.simulated_data)
	def returnStepSize(self, index):
		return self.Y[index]
	def returnStepSizes(self):
		return self.Y
#	def plot(self):
		#plt.plot(self.x, self.Y, 'b-')
		#plt.plot(self.x[:self.size], self.simulated_data, '')
		#xx=1
		#xPt = [xx,xx]
		#yLine = [0,self.Y[xx]]
		#plt.plot(xPt, yLine, 'k-')
		#plt.show()
