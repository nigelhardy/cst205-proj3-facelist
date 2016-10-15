"""
	facelist.py
	Abstract: This is a photobooth apllication with a twist. The photobooth analyzes your facial emotion and plays a song 
			that matches matches the emotion. 
	Author(s): Nigel Hardy, Ryan Cruz, Brandon Avery 
	GitHub:  https://github.com/nigelhardy/cst205-proj2-facelist
"""

import platform
system = platform.system()

if system == 'Windows':
	import cv2
	import numpy
	from matplotlib import pyplot as plt
	import PIL.Image as im
	import PIL.ImageTk as imTk
	import threading
	from tkinter import *

else:
	import cv2
	import numpy
	from matplotlib import pyplot as plt
	import PIL.Image as im
	import PIL.ImageTk as imTk
	import threading
	from Tkinter import *
import gui

root = Tk()
app = gui.Application(master=root)
app.master.title("Facelist - Powered by SoundCloud")
app.after(500, app.updateFrame)
app.updateCam()
app.mainloop()