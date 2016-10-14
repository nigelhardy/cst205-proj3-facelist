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