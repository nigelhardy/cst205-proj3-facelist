

import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd
from PIL import Image as im
import os
import glob
import time


class Browser(Frame):
	def __init__(self, master = None):
		Frame.__init__(self,master)
		self.fileList = []
		self.createWidgets()

	def createWidgets(self):
		self.initText = "Choose 5 Images to create photostrip"
		self.label = Label(text=self.initText)
		self.browseBtn = Button(text = "Create Photostrip", command = self.browseFile)
		self.browseBtn.grid(row=3,column=2, rowspan = 2, columnspan=2)
		self.label.grid(row=1,column=1,rowspan=2,columnspan=2);
	def browseFile(self):
		browse = fd.askopenfilenames(multiple=True, title = "Choose 5 Images (use ctrl)")
		self.fileList = root.tk.splitlist(browse)
		# print(self.fileList)
		self.createStrip()

	def createStrip(self):
		timestamp = time.strftime("%a_%d%b%Y_%H.%M.%S")
		if len(self.fileList) == 5:
			count = 0
			newImage = im.new('RGB', (1000,2800),(255,255,255))
			for f in self.fileList:
				if count == 0:
					start = (100,50)
					count+=1
				else:
					ystart = 50 + (count*550)
					start = (100,ystart)
					count+=1
				image = im.open(f);
				resized = image.resize((800,500));
				newImage.paste(resized,start)
			newImage.save("photostrips/%s.jpg"%timestamp)
			newImage.show()
		else:
			self.initText = "CHOOSE 5 IMAGES (NO MORE OR LESS)."
			self.label.config(fg='red')


root = Tk()
app = Browser(master=root)
app.mainloop()
