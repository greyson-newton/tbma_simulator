from tkinter import *
from sim_remote import *
from dataManager import *
import datetime, os, math

#Save residual Plots Option
#Make residual PLots a part of chamber plot's figure
#Labels for each plot

debug = False

window = Tk()
window.title("Muon Simulator")

time1 = ''
clock = Label(window, font=('times', 20, 'bold'), bg='green')
#print(len(axs), len(axss))
menubar = Menu(window)
optionmenu = Menu(menubar, tearoff = 0)
datamenu = Menu(menubar, tearoff = 0)

optionmenu.add_command(label = "Show Text Log", command = lambda: showLog())
optionmenu.add_command(label = "Show Plot", command = lambda: showPlots())
optionmenu.add_command(label = "Show Spread Sheet", command = lambda: showSpreadSheet())
optionmenu.add_separator()

datamenu.add_command(label = "Sort by Time", command = lambda: sortByTime())
datamenu.add_command(label = "Sort by nIterations", command = lambda: sortByIterations())

menubar.add_cascade(label = "Options", menu = optionmenu)
menubar.add_cascade(label = "Data Options", menu = datamenu)
sim_remote = sim_remote()

pred_x, pred_y, pred_z, pred_phi = 0,0,0,0
dz, dy, dx, dphi = 0,0,0,0
act_x, act_y, act_z, act_phi = 0,0,0,0

count = 0
momentum = 0

runsLabel = Label(window, text = 'nRuns').grid(row=0, column=0)
runsEntry = Entry(window, width=12, bd = 2)
runsEntry.grid(row = 1, column = 0)
runsEntry.insert(0, '1')

accuracyLabel = Label(window, text="Accuracy").grid(row = 0, column = 1)
accuracyEntry = Entry(window, width=12, bd = 2)
accuracyEntry.grid(row=1, column=1)
accuracyEntry.insert(0, "0.000001")

momentumLabel = Label(window, text="Momentum").grid(row=0, column=2)
momentumEntry = Entry(window, width=12, bd = 2)
momentumEntry.grid(row=1, column=2)
momentumEntry.insert(0, "AUTO")

size_label = Label(window, text="Chamber size : (w,h) ").grid(row=0, column=4)
size_Entry = Entry(window, width=12, bd = 2)
size_Entry.grid(row=1, column = 4)
size_Entry.insert(0, "(10,10)")

blank = Label(window,text="").grid(row=8,column=3)

des_pos_Label = Label(window, text="Design Position : (x,y,z)").grid(row=2, column=0)
des_pos_Entry = Entry(window, width=12, bd = 2)
des_pos_Entry.grid(row=2,column=1)
des_pos_Entry.insert(0, "(50,0,0)")

act_pos_Label =Label(window, text=" misaligned by : (dx,dy,dz)").grid(row=2, column=3)
act_pos_Entry = Entry(window, width=12, bd = 2)
act_pos_Entry.grid(row=2,column=2)
act_pos_Entry.insert(0, "(5,0,0)")

des_rot_Label = Label(window, text="Design Rotation : (theta,eta,phi)").grid(row=3, column=0)
des_rot_Entry = Entry(window, width=12, bd = 2)
des_rot_Entry.grid(row=3,column=1)
des_rot_Entry.insert(0, "(0,0,0)")

act_rot_Label = Label(window,text=" misaligned by: d(theta,eta,phi)").grid(row=2,column=1)
act_rot_Entry = Entry(window, width=12, bd = 2)
act_rot_Entry.grid(row=2,column=2)
act_rot_Entry.insert(0, "(0,0,0)")

#theta is a rotation around the x axis, in the x-y plane 
#eta is a rotation around the y axis, in the x-z plane
#phi is a rotation around the z axis, in the x-y plane

completionString = StringVar()
completionString.set("0 jobs complete out of: 0")
StartBtn = Button(window,text="Start", command=lambda: start()).grid(row=4, column=0)
completionLabel = Label(window, textvariable=completionString).grid(row =7, column = 1)

def start():
	init_simulation()
	nRuns = int(runsEntry.get())
	momentum = momentumEntry.get()
	acc = float(accuracyEntry.get())
	design_values=[]
	actual_values=[]
	chamber_values=[]
	fill_sim_data(zip(str(des_pos_Entry.get()).split(','), 
										str(des_rot_Entry.get()).split(','),
										str(act_pos_Entry.get()).split(','), 
										str(act_rot_Entry.get()).split(','),
										str(size_Entry.get()).split(',')))
	muon_blast()
	update_plotter()
def showLog():
	sim_remote.showLog()
	#e.msgbox('Cannot open Log', 'wait until program is finished')
def showSpreadSheet():
	sim_remote.showSpreadSheet()
def showPlots():
	sim_remote.showPlots()
def sortByTime():
	sim_remote.setSortingFilter("time")
def sortByIterations():
	sim_remote.setSortingFilter("iterations")


window.config(menu=menubar)

window.mainloop()

