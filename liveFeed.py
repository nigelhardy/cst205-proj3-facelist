"""
	liveFeed.py
	Abstract:
		This class will return a continuous stream of frames from the webcam until a button is pressed.
		Once the 'flag' is pressed, the feed will pause or wait for 5-	1o seconds and show the image that 
		was taken. The image will be saved and then passed onward to the next module.
"""

import numpy as np
import cv2 as cv
import time as t


class liveFeed:
	def __init__(self):
		super().__init__cv.VideoCapture(0)



def liveStream():


#function captures a single image, then shows image
def captureImage(flag):
	
