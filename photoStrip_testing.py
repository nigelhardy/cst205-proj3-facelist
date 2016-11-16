"""
	Testing material for creating a photostrip.
	Will be creating modules for creating thumbnails and stitching images together.
	
"""

from PIL import Image as im
import os
import glob

path = "testImages/"
listg = glob.glob1(path, '*.jpg')
newImage = im.new('RGB', (800,2500))
count = 0;
for f in  listg: 
	if count == 0:
		start = (0,0)
		count+=1
	else:
		start = (0,(count*500))
		count+=1
	image = im.open(path+f);
	resized = image.resize((800,500),im.BILINEAR);
	newImage.paste(resized,start)

newImage.show()