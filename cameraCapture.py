# cameraCapture.py
# 	This module should read images from the users camera and save them as image arrays.
#Joshua Ryan Cruz

import numpy as np
import cv2 as cv 
import tkinter as tk 



cv.namedWindow("preview")
vidCamera = cv.VideoCapture(0)
path = "C:/Users/Ryan Cruz/Documents/CSIS/CST205/Pro1Images/"
count = 1;
tkRoot = Tk()
root.title = 'LiveStream'

mainFrame = tk.Frame(root, )

def app():
	tkRoot = Tk()
	root.title = 'LiveStream'
	mainFrame = tk.Frame(root, )

if vidCamera.isOpened():
	rval, frame = vidCamera.read()
else:
	rval = false

while(rval):
	cv.imshow("preview", frame)
	rval, frame = vidCamera.read()
	key = cv.waitKey(20)
	if key == 32:
		rval, capFrame = vidCamera.read()
		cv.imwrite("cap%d.jpg"% count,capFrame)
		count+=1
		cv.namedWindow("lastimage")
		cv.imshow("lastimage",capFrame) 
	if key == 27:
		break
cv.destroyWindow("preview")
#cv.imshow("lastimage",lastimage)	


