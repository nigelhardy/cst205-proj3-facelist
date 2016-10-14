"""
	liveFeed.py
	Abstract:
		This class will return a continuous stream of frames from the webcam until a button is pressed.
		Once the 'flag' is pressed, the feed will pause or wait for 5-	1o seconds and show the image that 
		was taken. The image will be saved and then passed onward to the next module.
"""
import numpy as np
import cv2 as cv
import PIL.ImageTk as ImageTk
from PIL import Image
import time as t
import tkinter as tk
#class contains flad for when to pause 
class liveFeed:
	def __init__(self):
		self.cam = cv.VideoCapture(0)
		#self.flag = flag
		self.count = 1


	#checks to see if videoCapture is opened
	def isOpen(self):
		if self.cam.isOpened():
			return True
		else:
			return False

	def set(self,propID, value):
		self.cam.set(propID,value)


	#stream from cv Video object
	#returns images as tk image objects. 
	#lmain is a label object
	def stream(self):
		if self.isOpen():
			running, frame = self.cam.read()
		else: 
			running = self.cam.open(0)
		_, frame = self.cam.read()
		frame = cv.flip(frame, 1)
		cvimage = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)
		img = Image.fromarray(cvimage)
		return img

	#function captures a single image
	def captureImage():
		rval, capFrame = self.cam.read()
		success = cv.imwrite("cap%d.jpg"% count,capFrame)
		count+=1
		return (success,capFrame)

	def start(self):
		self.stream()

	def stop(self): 
		self.cam.release()



	
