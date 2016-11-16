#Author:  Nigel Hardy
#Created:  10/14/2016
#CSUMB CST-205 Project 3
#Team 40
#GitHub:  https://github.com/nigelhardy/cst205-proj3-facelist

'''
Multithreading thoughts:
Add anything that needs to be done to the queue
loop is always going through queue and adding to thread, have 4 threads maybe, no more
Lock and release printStuff
global vars picked out that get changed


'''

import cv2
import numpy
from matplotlib import pyplot as plt
import PIL.Image as im
import PIL.ImageTk as imTk
#from PIL import ImageTk as imTk
import os
from tkinter import *
import emotionRecognition
import facelistAudio as flAudio
import soundcloud
import threading
import time
from threading import Thread
import queue

q = queue.Queue()

global songNames # array of strings to fill Tkinter labels
songNames = []
songNames.append("Song Name:")
songNames.append("--NOT SET--")
songNames.append("Emotion:")
songNames.append("--NOT SET--")
songNames.append("Powered by SoundCloud")




class Application(Frame): # class for gui

    def playSongSC(self): # plays the song from emotion string
        try: # catches exception so that gui doesn't freeze indefinitely
            audio = flAudio.facelistAudio() # init soundcloud library
            # neutral isn't a great keyword, so only use emotion if we didn't get neutral
            if songNames[3] != "Neutral": 
                audio.getSong(songNames[3].lower())
            else:
                audio.getSong("relaxing") #used instead of neutral
            songNames[1] = audio.getTrackTitle() 
            # updates gui to song name
            self.songLabels[1]["text"] = songNames[1]
            songNames[4] = "Found song."
            self.songLabels[4]["text"] = songNames[4]
            if audio.retSizeArr() > 0:
                audio.playSongs()
        except:
            print("Couldn't play song")
    
    
    def switchBool(self): # turns on and off the webcam feed
        self.updateB = not self.updateB
        if self.updateB is True:
            self.actButton["text"] = "Camera Activated"
            self.updateFrame()
        else:
            self.actButton["text"] = "Camera Deactivated"

    def updateFrame(self): # updates gui
        '''if self.updateB is True:
            self.count = 0
            self.songLabels[0] = self.c
            for s in songNames:
                self.songLabels[self.count]["text"] = s
                self.count += 1
            #self.updateCam()
            '''
        
        while not q.empty():
            thread = Thread(target=q.get())
            thread.start()
            q.task_done()
        q.join()
        self.after(10, self.updateFrame)
    def tryThreading(self):
        q.put(self.printSome)
        q.put(self.changeText)
            #self.after(self.speed, self.updateFrame)
    def changeText(self):
        self.actButton["text"] = str(self.numCount)
    def printSome(self):
        self.numCount += 1

    def updateCam(self): #updates webcam feed
        _, frame = self.webcam.read() # reads from webcam
        frame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        self.img = im.fromarray(cv2image)
        imgtk = imTk.PhotoImage(image=self.img) #converts to proper image format
        self.webcamLbl.imgtk = imgtk 
        self.webcamLbl.configure(image=imgtk) # puts img into gui

    def createWidgets(self):
        # image below is used as a placeholder, this is the only way i could get the video to 
        # show up. 

        # various numbers for formatting
        lastRow = 17
        numCols = 3
        self.wid = 30
        self.wrp = 200
        pdx = 15
        #initializes different 'widgets' in Tkinter
        image = im.open("your-image.jpg") 
        image = image.resize((300,300), im.BILINEAR)
        photo = image
        imgtk = imTk.PhotoImage(image=image)
        self.webcamLbl = Label(self, image=imgtk)
        
        self.webcamLbl.grid(row=1,column=3,columnspan=1, rowspan=lastRow-2)
        self.webcamLbl.image = imgtk

        self.actButton = Button(self, text="Camera Activated", borderwidth=2, command=self.switchBool, width=self.wid)
        self.actButton.grid(row=1, column=0, columnspan=3, sticky=W, padx=pdx)
        # Labelss containing text
        self.songLbl = Label(self, text="Temp1", borderwidth=2, wraplength=self.wrp, padx=10, anchor=W, justify=LEFT, width=self.wid)
        self.songLbl.grid(row=2,column=0, columnspan=3)
        self.songLabels.append(self.songLbl)
        self.songLbl = Label(self, text="Temp2", wraplength=self.wrp, padx=pdx, anchor=W, justify=LEFT, width=self.wid)
        self.songLbl.grid(row=3,column=0, columnspan=3)
        self.songLabels.append(self.songLbl)
        self.songLbl = Label(self, text="Temp3", wraplength=self.wrp, padx=pdx, anchor=W, justify=LEFT, width=self.wid)
        self.songLbl.grid(row=4,column=0, columnspan=3)
        self.songLabels.append(self.songLbl)
        self.songLbl = Label(self, text="Temp4", wraplength=self.wrp, padx=pdx, anchor=W, justify=LEFT, width=self.wid)
        self.songLbl.grid(row=5,column=0, columnspan=3)
        self.songLabels.append(self.songLbl)
        self.songLbl = Label(self, text="Temp5", wraplength=self.wrp, padx=pdx, anchor=W, justify=LEFT, width=self.wid)
        self.songLbl.grid(row=8,column=0, columnspan=3)
        self.songLabels.append(self.songLbl)
        # buttons
        self.btnPlay = Button(self, text="Play Song", width=self.wid, height=4)
        self.btnPlay.grid(row=lastRow-8, column=0, columnspan=3, rowspan=4, padx=pdx, sticky=W)
        self.btnPlay["command"] = self.updateFrame

        self.btnPic = Button(self, text="Take Picture", width=self.wid, height=4)
        self.btnPic.grid(row=lastRow-4, column=0, columnspan=3, rowspan=4, padx=pdx, pady=10, sticky=W)
        self.btnPic["command"] = self.tryThreading

    def takethephoto(self): #updates gui before taking photo
        songNames[4] = "Analyzing Photo..."
        #self.songLabels[4]["text"] = songNames[4]
        self.after(50, self.take_photo) #takes photo after 50 milliseconds

    def take_photo(self):
        if(self.webcam.isOpened()):
            if self.updateB is True:
                _, frame = self.webcam.read()
                success = cv2.imwrite("cap%d.jpg"% self.count,frame) #saves photo
                self.count += 1
                frame = cv2.flip(frame, 1)
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) # converts colors/image
                self.img = im.fromarray(cv2image)
                img_array = emotionRecognition.faceLocalization(self.img) #analyzes photo
                imgtk = imTk.PhotoImage(image=self.img) # converts photo to Tk Image
                self.webcamLbl.imgtk = imgtk
                self.photoTaken = True
                songNames[3] = emotionRecognition.retEmotion(img_array)  # gets emotion most likely found 
                songNames[4] = "Photo has been taken."
        return imgtk
    
    def playSongAfter(self):
        if self.photoTaken is True:
            songNames[4] = "Finding Song..."
            self.songLabels[4]["text"] = songNames[4]
            self.after(50, self.playSongSC)


    def __init__(self, master=None): # inializes gui and defines variables for class
        Frame.__init__(self, master)
        self.frame = Frame(master)
        self.songLabels = [] # list for names of songs
        self.actButton = Button() # activate webcam button
        self.webcamLbl = Label() # webcam image widget label
        self.photoTaken = False
        #self.webcam = cv2.VideoCapture(5)
        #self.img = self.webcam
        self.updateB = True # bool to start and stop webcam update
        self.pack() # prepare gui
        self.speed = 10 # milliseconds between UI refresh
        self.counter = 0
        self.count = 0
        self.createWidgets() # build gui
        self.c = 0
        self.numCount = 0


root = Tk() # initialize Tkinter variable
app = Application(master=root) # initialize Tkinter class
app.master.title("Facelist - Powered by SoundCloud") # Set title of window
#q.put(app.after(500, app.updateFrame)) #start the gui update function
#q.put(app.updateCam) # start the camera update function
app.mainloop() # enter Tkinter mainloop


'''
for i in range(20):
    q.put(i * i)

while not q.empty():
    print(q.get())
'''
'''
import sys
lock = threading.Lock()
global myNum
myNum = -1;
def myfunc():
    global myNum
    for x in range(0,10000):
        lock.acquire()
        myNum = x
        for n in range(0, 1000):
            n = n
        lock.release()
    print("x done " + str(x))
def myfunctwo():
    global myNum
    for y in range(0,10000):
        lock.acquire()  
        myNum = 100 - y      
        lock.release()
    print("y done " + str(100-y))
def printIt():
    for l in range(0, 100):
        lock.acquire()
        print(str(myNum))
        lock.release()

t = Thread(target=myfunc)
t.start()
z = Thread(target=myfunctwo)
z.start()
f = Thread(target=printIt)
f.start()
'''