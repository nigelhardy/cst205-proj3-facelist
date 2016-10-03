"""
	liveFeed.py
	Abstract:
		This class will return a continuous stream of frames from the webcam until a button is pressed.
		Once the 'flag' is pressed, the feed will pause or wait for 5-	1o seconds and show the image that 
		was taken. The image will be saved and then passed onward to the next module.
"""

import numpy as np
import cv2 as cv
import Image from PIL
import ImageTk from PIL
import time as t


#class contains flad for when to pause 
class liveFeed(cv.videoCapture):
	def __init__(self, flag):
		self.cam = super().__init__cv.VideoCapture(0)
		self.flag = flag
		self.count = 1;


#checks to see if videoCapture is opened
def isOpen(self):
	if cam.isOpened():
		return true
	else:
		return false

#stream from cv Video object
#returns images as tk image objects. 
def stream(self, flag):
	if self.isOpen():
		running, frame = self.cam.read()
	else: 
		running = self.cam.open(0)
	while(running):
		#cv.imshow("preview", frame)
		rval, frame = cam.read()
		image = ImageTk.PhotoImage(frame)
		return image

#function captures a single image
def captureImage():
		rval, capFrame = self.cam.read()
		waitKey(50)
		success = cv.imwrite("cap%d.jpg"% count,capFrame)
		count+=1
		return success;
	
