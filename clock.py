import tkinter as tk
from time import time

class Stopwatch:
    def __init__(self, timeElapsed, paused, window, button):

        self.timeElapsed = timeElapsed
        self.window = window
        self.paused = paused
        self.button = button
    def start(self):
        window.mainloop()
        toggle()
        run_timer()



def toggle(self):
    if self.paused:
        self.paused = False
        self.button.config(text='Stop')
        self.oldtime = time()
        self.run_timer()
    else:
        self.paused = True
        self.oldtime = time()
        self.button.config(text='Start')

def run_timer(self):
    if self.paused:
        return
    delta = int(time() - self.oldtime)
    timestr = '{:02}:{:02}'.format(*divmod(delta, 60))
    self.timeElapsed.config(text=timestr)
    self.timeElapsed.after(1000, self.run_timer)