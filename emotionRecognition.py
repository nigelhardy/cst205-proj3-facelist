#Author: Joshua Cruz
#Created:  10/14/2016
#CSUMB CST-205 Project 2
#Team 24
#GitHub:  https://github.com/nigelhardy/cst205-proj2-facelist
import numpy as np
from PIL import Image as im
from PIL import ImageEnhance as imEn
import indicoio as ind
import operator

ind.config.api_key = "18f4dba9b853159e163402e9ddba8abc"

# crops image to just the face
def faceLocalization(img): 
	enIm = imEn.Brightness(img)
	enhanced = enIm.enhance(1.5)
	im_array = np.array(enhanced)
	crop_loc = ind.facial_localization(im_array)
	topX = crop_loc[0]['top_left_corner'][0]
	topY = crop_loc[0]['top_left_corner'][1]
	bottomX = crop_loc[0]['bottom_right_corner'][0]
	bottomY = crop_loc[0]['bottom_right_corner'][1]
	cropped_im = enhanced.crop((topX,topY,bottomX,bottomY))
	cropped_array = np.array(cropped_im)
	return cropped_array


#data should be a PIL image
#gets probability of emotion from indico api
#sorts dictionary by value and returns string of highest probability emotion
def retEmotion(data):
	emoDict = ind.fer(data)
	sortedDict = sorted(emoDict.items(), key = operator.itemgetter(1))
	return sortedDict[5][0]

#img = im.open("cap1.jpg")
#img_array = faceLocalization(img)
#print(retEmotion(img_array))
