import numpy as np
from PIL import Image as im
from PIL import ImageEnhance as imEn
import indicoio as ind
ind.config.api_key = "18f4dba9b853159e163402e9ddba8abc"


def faceLocalization(data):
	img_array = ind.facial_localization(data)
	return img_array

#data should be a PIL image
def retEmotion(data):
	emoDict = ind.fer(data)
	highProb = {}
	for key in emoDict:
		print(key +":" + "%0.4f"%emoDict[key])
		# print(value)
	# for(key in emoDict):
	# 	if(d[key] > 0.05):
	# 		highProb[key] = emoDict[key]
	# for x in highProb:
	# 	if((x+1) < highProb.len()):
	# 		sorted(highProb.values())

img = im.open("cap22.jpg")
enIm = imEn.Brightness(img)
enhanced = enIm.enhance(1.5)
im_array = np.array(enhanced)
crop_loc = faceLocalization(im_array)
topX = crop_loc[0]['top_left_corner'][0]
topY = crop_loc[0]['top_left_corner'][1]
bottomX = crop_loc[0]['bottom_right_corner'][0]
bottomY = crop_loc[0]['bottom_right_corner'][1]
print(topX,topY,bottomX,bottomY)
cropped_im = enhanced.crop((topX,topY,bottomX,bottomY))
cropped_array = np.array(cropped_im)
cropped_im.show()

retEmotion(cropped_array)
