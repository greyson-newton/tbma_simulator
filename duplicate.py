from tkinter import *
import matplotlib.pyplot as plt
from Stopwatch import *
from AI_Remote import *
import easygui as e
import datetime, os, math

#Save residual Plots Option
#Make residual PLots a part of chamber plot's figure
#Labels for each plot


class Stopwatch:
	def __init__(self, label):
		self.label = label
		self.counter = -1
		self.running = False
		print("stopwatch created, running false")
	def counter_label(self, label): 
		if self.running and self.counter == -1:
			print("running is true, but first second")
			self.initTime = time.time()
			self.label = label
			label.config(text=(initTime-initTime))
			print("initialy working")
		else:
			if(self.running and not(self.counter == -1)):
				self.delTime = time.time() - initTime
				labelDisplay = newTime - initTime
				self.label.after(1000, labelDisplay)
				counter += 1
	def addTime(time, delTime):
		return time+delTime
	def Start(self, label): 
	    global running 
	    running=True
	    


###################################################################

def start():
	#progressWindow = Tk()
	#progressWindow.title = "Progress"
	stopwatch.Start(timeElapsed)
	stopwatch.counter_label(timeElapsed)
	print("start")
	#nJobs = 0
	#xI, xF, xB, yI, yF, yB, pI, pF, pB = 0,0,0,0,0,0,0,0,0
	#getRanges(xI, xF, xB, yI, yF, yB, pI, pF, pB, nJobs)
	dxValues = str(dxEntry.get()).split(',')
	dyValues = str(dyEntry.get()).split(',')
	dpValues = str(dPhiEntry.get()).split(',')
	xI, xF, xB = float(dxValues[0]), float(dxValues[1]), float(dxValues[2])
	yI, yF, yB = float(dyValues[0]), float(dyValues[1]), float(dyValues[2])
	pI, pF, pB = float(dpValues[0]), float(dpValues[1]), float(dpValues[2])
	print(xI, xF, xB, yI, yF, yB, pI, pF, pB)
	AI_remote.start(float(xEntry.get()), float(yEntry.get()), float(phiEntry.get())*(math.pi/180), xI, xF, xB, yI, yF, yB, pI, pF, pB, int(lengthEntry.get()), float(accuracyEntry.get()))
# start function of the stopwatch 

def showLog():
	try:
		AI_remote.showLog()
	except:
		e.msgbox('Cannot open Log', 'wait until program is finished')

def showPlots():
	AI_remote.showPlots()
	e.msgbox('Cannot show Plots', 'wait until program is finished')


fig = plt.figure(figsize = (10,6))
sub1 = plt.subplot(3,2,1)
sub2 = plt.subplot(3,2,3)
sub3 = plt.subplot(3,2,5)
sub4 = plt.subplot(3,2,2)
sub5 = plt.subplot(3,2,4)
sub6 = plt.subplot(3,2,6)
#axs = plt.subplots(nrows=3, ncols=2, sharex=True, sharey=True, figsize = (10,6), gridspec_kw={'hspace': 0})
fig.suptitle('Top 3 Jobs')


sub1.margins(0.05)
sub1.set_xlim([0,60])
sub1.set_ylim([-100, 100])

sub2.margins(0.05)
sub2.set_xlim([0,60])
sub2.set_ylim([-100, 100])

sub3.margins(0.05)
sub3.set_xlim([0,60])
sub3.set_ylim([-100, 100])

window = Tk()
window.title("Muon Simulator")

time1 = ''
clock = Label(window, font=('times', 20, 'bold'), bg='green')
#print(len(axs), len(axss))
menubar = Menu(window)
optionmenu = Menu(menubar, tearoff = 0)
optionmenu.add_command(label = "Show Log", command = lambda: showLog())
optionmenu.add_command(label = "Show Plot", command = lambda: showPlots())
optionmenu.add_separator()
menubar.add_cascade(label = "Options", menu = optionmenu)
AI_remote = AI_Remote(fig, sub1, sub2, sub3, sub4, sub5, sub6)
X, Y, Phi = 0,0,0
Dx, Dy, dPhi = 0,0,0
count = 0

designPosLabel = Label(window, text="Enter Design Pos:").grid(row=3, column=0)
actualPosLabel =Label(window, text="Enter Actual Range:").grid(row=5, column=0)
blank1 = Label(window,text="").grid(row=6,column=3)

xLabel = Label(window,text="X").grid(row=2,column=1)
yLabel = Label(window,text="Y").grid(row=2,column=2)
phiLabel = Label(window,text="Phi").grid(row=2,column=3)

DXLabel = Label(window,text="DX").grid(row=4,column=1)
DYLabel = Label(window,text="DY").grid(row=4,column=2)
DPhiLabel = Label(window,text="DPhi").grid(row=4,column=3)

accuracyLabel = Label(window, text="Accuray").grid(row = 0, column = 1)
lengthLabel = Label(window, text="Length").grid(row=0, column=3)
blank = Label(window,text="").grid(row=8,column=3)



accuracyEntry = Entry(window)
accuracyEntry.grid(row=1, column=1)
accuracyEntry.insert(0, "0.0001")
lengthEntry = Entry(window)
lengthEntry.grid(row=1, column = 3)
lengthEntry.insert(0, "100")


xEntry = Entry(window)
xEntry.grid(row=3,column=1)
xEntry.insert(0, "50")
yEntry = Entry(window)
yEntry.grid(row=3,column=2)
yEntry.insert(0, "0")
phiEntry = Entry(window)
phiEntry.grid(row=3,column=3)
phiEntry.insert(0, "90")
phiEntry.config(state='readonly')

dxEntry = Entry(window)
dxEntry.grid(row=5,column=1)
dxEntry.insert(0, "0,5,5")
dyEntry = Entry(window)
dyEntry.grid(row=5,column=2)
dyEntry.insert(0, "0,0,0")
dPhiEntry = Entry(window)
dPhiEntry.grid(row=5,column=3)
dPhiEntry.insert(0, "0,0,0")
StartBtn = Button(window,text="Start", command=lambda: start()).grid(row=7, column=0)
#ShowBtn = Button(window, text="Show", command=lambda: showPlots()).grid(row=9, column=3)
#LogBtn = Button(window, text="Log", command=lambda: showLog()).grid(row = 9, column=2)

timeLabel = Label(window, text="Time Elapsed:").grid(row = 7, column = 1)
timeElapsed = Label(window, text="00:00", width=20).grid(row = 7, column = 2)
stopwatch = Stopwatch(timeElapsed)

window.config(menu=menubar)
window.mainloop()