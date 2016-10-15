'''Authors:  Nigel Hardy, Brandon Avery, Joshua Cruz
Created:  10/14/2016
CSUMB CST-205 Project 2: Facelist
Team 24
GitHub:  https://github.com/nigelhardy/cst205-proj2-facelist

GUI - Nigel Hardy
Audio - Brandon Avery
Webcam and Indico (emotion) - Joshua Cruz

Facelist analyzes your emotion through a webcam 
photo and plays a song from soundcloud to match your mood
'''
import cv2
import numpy
from matplotlib import pyplot as plt
import PIL.Image as im
import PIL.ImageTk as imTk
import threading
import os
if os.name != "nt":
	from Tkinter import *
else:
	from tkinter import *
import gui

root = Tk() # initialize Tkinter variable
app = gui.Application(master=root) # initialize Tkinter class
app.master.title("Facelist - Powered by SoundCloud") # Set title of window
app.after(500, app.updateFrame) #start the gui update function
app.updateCam() # start the camera update function
app.mainloop() # enter Tkinter mainloop