from expDecay import *
xinit, xfinal = 0, 10
expFit = expDecay(xinit, xfinal, 1.67)
stepSize = expFit.returnStepSize(0)
print(stepSize)
#expFit.plot()