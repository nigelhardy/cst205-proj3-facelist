# cameraCapture.py
# 	This module should read images from the users camera and save them as image arrays.
#Joshua Ryan Cruz

# import numpy as np
# import cv2 as cv 
# import tkinter as tk 
# import PIL.ImageTk as imTk
import liveFeed
import tkinter as tk
import cv2
from PIL import Image, ImageTk
 

root = tk.Tk()
root.bind(33, lambda e: root.quit())
lmain = tk.Label(root)
lmain.pack()
width, height = 800, 600
feed = liveFeed.liveFeed()
feed.set(cv2.CAP_PROP_FRAME_WIDTH, width)
feed.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


def show_stream():
	imgS = feed.stream()
	imgtk = ImageTk.PhotoImage(image=imgS)
	lmain.imgtk = imgtk
	lmain.configure(image=imgtk)
	lmain.after(100, show_stream())



def show_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(100, show_frame())

root.mainloop()

# def cap_frame(flag):
 	
 	# if key == 27:

# show_frame()
#</escape>
# def app():
# 	root = tk.Tk( )
# 	feed = liveFeed.liveFeed()
# 	tk.Label(root, text='Welcome to Facelist', borderwidth=2).grid(row=0,column=0)

# 	image = feed.stream()

# 	image = image.resize((300,300), im.BILINEAR)

# 	photo = imTk.PhotoImage(img=image)

# 	lbl1 = tk.Label(image=photo, anchor=NW)

# 	lbl1.image = photo

# 	lbl1.grid(row=0,column=1)

# 	btn1 = Button()

# 	btn1["text"] = "Take Picture"

# 	btn1.grid(row=1, column=1)

# 	root.mainloop( )



	# feed = liveFeed.liveFeed()
	# tkRoot = tk.Toplevel()
	# tkRoot.title = 'LiveStream'
	# img = feed.stream()
	# lf = tk.Label(tkRoot, image = img)
	
	# lf.pack

#app()

# if vidCamera.isOpened():
# 	rval, frame = vidCamera.read()
# else:
# 	rval = false

# while(rval):
# 	cv.imshow("preview", frame)
# 	rval, frame = vidCamera.read()
# 	key = cv.waitKey(20)
# 	if key == 32:
# 		rval, capFrame = vidCamera.read()
# 		cv.imwrite("cap%d.jpg"% count,capFrame)
# 		count+=1
# 		cv.namedWindow("lastimage")
# 		cv.imshow("lastimage",capFrame) 
# 	if key == 27:
# 		break
# cv.destroyWindow("preview")
# #cv.imshow("lastimage",lastimage)	


