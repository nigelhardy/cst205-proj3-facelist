import cv2
import numpy
from matplotlib import pyplot as plt
import PIL.Image as im
import PIL.ImageTk as imTk
import threading
from Tkinter import *
import emotionRecognition
import facelistAudio as flAudio
import soundcloud
import thread


global songNames
songNames = []
songNames.append("Song Name:")
songNames.append("--NOT SET--")
songNames.append("Emotion:")
songNames.append("--NOT SET--")
songNames.append("Powered by SoundCloud")

class Application(Frame):

    def playSongSC(self, songNm):
        try:
            audio = flAudio.facelistAudio()
            audio.getSong('happy')
            songNames[1] = audio.getTrackTitle()
            songNames[4] = "Finding song..."
            self.updateFrame()
            if audio.retSizeArr() > 0:
                audio.playSongs()
        except:
            print "Couldn't play song"

    def switchBool(self):
        self.updateB = not self.updateB
        if self.updateB is True:
            self.actButton["text"] = "Camera Activated"
            self.updateFrame()
        else:
            self.actButton["text"] = "Camera Deactivated"

    def updateFrame(self):
        if self.updateB is True:
            self.count = 0
            for s in songNames:
                self.songLabels[self.count]["text"] = s
                self.count += 1
            self.updateCam()
            self.after(self.speed, self.updateFrame)
    def updateCam(self):
        _, frame = self.webcam.read()
        frame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        self.img = im.fromarray(cv2image)
        imgtk = imTk.PhotoImage(image=self.img)
        self.webcamLbl.imgtk = imgtk
        self.webcamLbl.configure(image=imgtk)
        #self.webcamLbl.after(sp,self.updateCam)

    def createWidgets(self):
        # image below is used as a placeholder, this is the only way i could get the video to 
        # show up. 
        lastRow = 17
        numCols = 3
        self.wid = 30
        self.wrp = 200
        pdx = 15

        image = im.open("your-image.jpg") 
        image = image.resize((300,300), im.BILINEAR)
        photo = imTk.PhotoImage(image)
        self.webcamLbl = Label(self, image=photo)
        self.webcamLbl.grid(row=1,column=3,columnspan=1, rowspan=lastRow-2)
        self.webcamLbl.image = photo
        self.actButton = Button(self, text="Camera Activated", borderwidth=2, command=self.switchBool, width=self.wid)
        self.actButton.grid(row=1, column=0, columnspan=3, sticky=W, padx=pdx)
        
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

        self.btnPlay = Button(self, text="Play Song", width=self.wid, height=4)
        self.btnPlay.grid(row=lastRow-8, column=0, columnspan=3, rowspan=4, padx=pdx, sticky=W)
        self.btnPlay["command"] = self.playSoundCloudSong

        self.btnPic = Button(self, text="Take Picture", width=self.wid, height=4)
        self.btnPic.grid(row=lastRow-4, column=0, columnspan=3, rowspan=4, padx=pdx, pady=10, sticky=W)
        self.btnPic["command"] = self.take_photo_demo
        
    def take_photo_demo(self):
        if(self.webcam.isOpened()):
            if self.updateB is True:
                _, frame = self.webcam.read()
                success = cv2.imwrite("cap%d.jpg"% self.count,frame)
                self.count += 1
                frame = cv2.flip(frame, 1)
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                self.img = im.fromarray(cv2image)
                img_array = emotionRecognition.faceLocalization(self.img)
                #self.after(1500, self.changeSpeedBack)
                imgtk = imTk.PhotoImage(image=self.img)
                self.webcamLbl.imgtk = imgtk
                #self.speed = 1600
                self.photoTaken = True
                songNames[3] = emotionRecognition.retEmotion(img_array)   
                songNames[4] = "Photo has been taken."
        return imTk
    def changeSpeedBack(self):
        self.speed = 10

    def playSoundCloudSong(self):
        
        if self.photoTaken is True:
            
            songNames[4] = "Finding song..."
            self.updateFrame()
            self.switchBool()
            self.playSongSC(songNames[3].lower())
            
            #try:
                #thread.start_new_thread(  )
            #except:
                #print "no go"
        #c = 0

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.frame = Frame(master)
        self.songLabels = [] # list for names of songs
        self.actButton = Button() # activate webcam button
        self.webcamLbl = Label() # webcam image widget label
        self.photoTaken = False
        self.webcam = cv2.VideoCapture(0)
        self.img = self.webcam
        self.updateB = True # bool to start and stop webcam update
        self.pack() # prepare gui
        self.speed = 10 # milliseconds between UI refresh
        self.counter = 0
        self.count = 0
        self.createWidgets() # build gui
