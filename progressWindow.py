from tkinter import *

class progressWindow:
	def __init__(self):

		self.progressWin = Tk()
		screen_width = self.progressWin.winfo_screenwidth()
		screen_height = self.progressWin.winfo_screenheight()
		self.progressWin.title('Progress')
		self.progressWin.geometry('200x200')
		self.completionVar = StringVar()
		self.completionVar.set('Progress...')
		self.progressLabel = Label(self.progressWin, textvariable=self.completionVar)
		self.progressWin.mainloop()
	def updateProgress(self, jobNumber, nJobs):
		self.completionVar.set(str(jobNumber) + ' complete out of: ' + str(nJobs))
		#self.progressWin.update_idletasks()
		