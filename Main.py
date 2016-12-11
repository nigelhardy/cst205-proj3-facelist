#! /usr/bin/python
# -*- coding: utf-8 -*-
#
"""Special thanks to Patrick Fay
Parts of his program are used and made available via GNU Public License v2
"""
#Author:  Nigel Hardy (and Brandon and Ryan)
#Created:  11/20/2016
#CSUMB CST-205 Project 3
#Team 24
#GitHub:  https://github.com/nigelhardy/cst205-proj3-facelist

# import external libraries
import vlc
import twitter
import sys
import cv2
import numpy
from matplotlib import pyplot as plt
import PIL.Image as im
import PIL.ImageTk as imTk

if sys.version_info[0] < 3:
    import Tkinter as Tk
    from Tkinter import ttk
    from Tkinter.filedialog import askopenfilename
    from Tkinter import filedialog as fd
else:
    import tkinter as Tk
    from tkinter import ttk
    from tkinter.filedialog import askopenfilename
    from tkinter import filedialog as fd

from urllib import request

# import standard libraries
import os
import pathlib
from threading import Thread, Event
import time
import platform
import emotionRecognition
import facelistAudio as flAudio
import soundcloud

global songNames # array of strings to fill Tkinter labels

songNames = []

token = "804025595612889088-rQcroYgshimqQM8j9l8tmPcLpVNslUn"
token_key = "mcg8xNdD98TthPulQF2Ah1IDlsP04AZLAVOEuKYQMHn5Q"
con_secret = "PkxBzJUmRthw3rAVMOXkhnJVU"
con_secret_key = "oDnCke8u3JsVGFN4vBaBeBSNfCaHHi099nD88TbYzy5ellE8I3"
new_status = "testing testing"

api = twitter.Api(consumer_key='PkxBzJUmRthw3rAVMOXkhnJVU',
consumer_secret='oDnCke8u3JsVGFN4vBaBeBSNfCaHHi099nD88TbYzy5ellE8I3',
access_token_key='804025595612889088-rQcroYgshimqQM8j9l8tmPcLpVNslUn',
access_token_secret='mcg8xNdD98TthPulQF2Ah1IDlsP04AZLAVOEuKYQMHn5Q')

#status = api.PostUpdate('I blank python-twitter!')

class ttkTimer(Thread):
    """a class serving same function as wxTimer... but there may be better ways to do this
    """
    def __init__(self, callback, tick):
        Thread.__init__(self)
        self.callback = callback
        self.stopFlag = Event()
        self.tick = tick
        self.iters = 0

    def run(self):
        while not self.stopFlag.wait(self.tick):
            self.iters += 1
            self.callback()

    def stop(self):
        self.stopFlag.set()

    def get(self):
        return self.iters

class Player(Tk.Frame):
    """The main window has to deal with events.
    """
    def __init__(self, parent, title=None):
        Tk.Frame.__init__(self, parent)
        self.songURL = "EMPTY"
        self.songLabels = [] # list for names of songs
        self.webcamLbl = ttk.Label() # webcam image widget label
        self.photoTaken = False
        self.webcam = cv2.VideoCapture(0)
        self.updateB = True # bool to start and stop webcam update
        self.lastURL = "EMPTY"
        self.speed = 10 # milliseconds between UI refresh
        self.songs = []
        self.songCounter = 0
        self.parent = parent
        self.emotion = ""
        self.shutter = 0
        self.curated = True
        if title == None:
            title = "tk_vlc"
        self.parent.title(title)
        self.topMaster = ttk.Frame(self.parent)
        self.topPanel = ttk.Frame(self.topMaster)
        self.topPanelR = ttk.Frame(self.topMaster)
        #self.songName = ttk.Label(self.topPanel, text="Song: N/A")
        self.songName = ttk.Label(self.topPanel, text="Song: N/A")
        self.artistName = ttk.Label(self.topPanel, text="Artist: N/A")
        self.emotionLabel = ttk.Label(self.topPanel, text="Emotion: N/A")
        self.webCamButton = ttk.Button(self.topPanelR, text="Webcam Active", command=self.activateWebcam, width=15)
        
        self.shutter = ttk.Button(self.topPanelR, text="Take Photo", command=self.takethephoto, width=15)
        photostripButton = ttk.Button(self.topPanelR, text="Photostrip", command=self.browseFile, width=15)

        self.songName.grid(row=0, column=0, sticky=Tk.W)
        self.artistName.grid(row=1,column=0, sticky=Tk.W)
        self.emotionLabel.grid(row=2, column=0, sticky=Tk.W)
        photostripButton.grid(row=1, column=1, sticky=Tk.E)
        self.shutter.grid(row=0, column=0, rowspan=2, sticky=Tk.E, ipady=13)
        self.webCamButton.grid(row=0, column=1, sticky=Tk.E)
        self.topPanel.pack(fill=Tk.BOTH, side=Tk.LEFT)
        self.topPanelR.pack(fill=Tk.BOTH, side=Tk.RIGHT)
        self.topMaster.pack(fill=Tk.BOTH, side=Tk.TOP)

        # The second panel holds controls
        self.player = None
        self.videopanel = ttk.Frame(self.parent)
        image = im.open("artwork/default.jpg") 
        photo = image
        imgtk = imTk.PhotoImage(image=image)
        
        self.webcamLbl = ttk.Label(self.videopanel,image=imgtk, text="Stream")
        self.webcamLbl.image = imgtk
        self.webcamLbl.pack(side=Tk.BOTTOM)
        self.videopanel.pack(fill=Tk.BOTH,expand=1)
        self.videopanel.pack_propagate(False)
        self.videopanel["width"] = 650
        self.videopanel["height"] = 500
        ctrlpanel = ttk.Frame(self.parent)
        pause  = ttk.Button(ctrlpanel, text="Pause", command=self.OnPause)
        play   = ttk.Button(ctrlpanel, text="Play", command=self.OnPlay)
        stop   = ttk.Button(ctrlpanel, text="Stop", command=self.OnStop)
        volume = ttk.Label(ctrlpanel, text="Volume")

        self.nextButton = ttk.Button(ctrlpanel, text="Next", command=self.OnNext)
        self.prevButton = ttk.Button(ctrlpanel, text="Previous", command=self.OnPrev)

        self.prevButton.pack(side=Tk.LEFT)
        pause.pack(side=Tk.LEFT)
        play.pack(side=Tk.LEFT)
        stop.pack(side=Tk.LEFT)
        self.nextButton.pack(side=Tk.LEFT)
        self.nextButton["state"] = "disabled"
        self.prevButton["state"] = "disabled"
        volume.pack(side=Tk.LEFT)

        self.volume_var = Tk.IntVar()
        self.volslider = Tk.Scale(ctrlpanel, variable=self.volume_var, command=self.volume_sel,
                from_=0, to=100, orient=Tk.HORIZONTAL, length=100)
        self.volslider.pack(side=Tk.LEFT)
        self.volume_var.set(50)

        ctrlpanel.pack(side=Tk.BOTTOM)



        ctrlpanel2 = ttk.Frame(self.parent)
        self.scale_var = Tk.DoubleVar()
        self.timeslider_last_val = ""
        self.timeslider = Tk.Scale(ctrlpanel2, variable=self.scale_var, command=self.scale_sel,
                from_=0, to=1000, orient=Tk.HORIZONTAL, length=500)
        self.timeslider.pack(side=Tk.BOTTOM, fill=Tk.X,expand=1)
        
        self.timeslider_last_update = time.time()
        ctrlpanel2.pack(side=Tk.BOTTOM,fill=Tk.X)

        ctrlpanel3 = ttk.Frame(self.parent)
        self.curated = Tk.IntVar()
        self.curateCheck = ttk.Checkbutton(ctrlpanel3, text="Curate", variable=self.curated)
        self.curated.set(1)
        self.curateCheck.pack(side=Tk.RIGHT)
        self.message = ttk.Label(ctrlpanel3, text="Status: Ready to take photo.")
        self.message.pack(side=Tk.LEFT)
        self.share = ttk.Button(ctrlpanel3, text="Share", command=self.share)
        self.share.pack(side=Tk.RIGHT)
        self.inputText = ttk.Entry(ctrlpanel3, width=15)
        self.inputText.pack(side=Tk.RIGHT)
        self.instruction = ttk.Label(ctrlpanel3, text="Your name: ")
        self.instruction.pack(side=Tk.RIGHT)
        
        ctrlpanel3.pack(fill=Tk.BOTH, side=Tk.TOP)

        # VLC player controls
        self.Instance = vlc.Instance()
        self.player = self.Instance.media_player_new()
        #self.player.audio_set_volume(100)
        self.timer = ttkTimer(self.OnTimer, 1.0)
        self.timer.start()
        self.parent.update()
    def share(self):
        user = self.inputText.get()
        if len(self.songs) > 0 and len(user) > 0:
            self.message["text"] = "Status: Sharing for you now " + user + "." 
            statusUpdate = self.inputText.get() + " felt " + self.songs[self.songCounter-1]["emotion"] + " and FaceList played " 
            statusUpdate += self.songs[self.songCounter-1]["track_title"] + " by " + self.songs[self.songCounter-1]["track_artist"]["username"]
            if len(statusUpdate) > 139:
                statusUpdate = statusUpdate[0:139]
            status = api.PostUpdate(statusUpdate)
        else:
            self.message["text"] = "Status: Take a photo and enter your name." 
        
    def OnNext(self):
        if len(self.songs) > 0 and self.songCounter < len(self.songs):
            self.songCounter += 1
            self.message["text"] = "Status: Selected " + str(self.songCounter) + " out of " + str(len(self.songs)) + "."
            self.songURL = self.songs[self.songCounter-1]["stream_url"]
            self.songName["text"] = "Song: " + self.songs[self.songCounter-1]["track_title"]
            self.artistName["text"] = "Artist: " + self.songs[self.songCounter-1]["track_artist"]["username"]
            self.emotionLabel["text"] = "Emotion: " + self.songs[self.songCounter-1]["emotion"]
            self.showImage(str(self.songCounter) + "_artwork.jpg")
            if self.songCounter - 1 > 0:
                self.prevButton["state"] = "normal"
            if self.songCounter >= len(self.songs):
                self.nextButton["state"] = "disabled"
            self.after(20, self.OnStop)


    def OnPrev(self):
        if len(self.songs) > 0 and self.songCounter - 1 > 0:
            self.songCounter -= 1
            self.message["text"] = "Status: Selected " + str(self.songCounter) + " out of " + str(len(self.songs)) + "."
            self.songURL = self.songs[self.songCounter-1]["stream_url"]
            self.songName["text"] = "Song: " + self.songs[self.songCounter-1]["track_title"]
            self.artistName["text"] = "Artist: " + self.songs[self.songCounter-1]["track_artist"]["username"]
            self.emotionLabel["text"] = "Emotion: " + self.songs[self.songCounter-1]["emotion"]
            self.showImage(str(self.songCounter) + "_artwork.jpg")
            if self.songCounter <= 1:
                self.prevButton["state"] = "disabled"
            if len(self.songs) > 0 and self.songCounter < len(self.songs):
                self.nextButton["state"] = "normal"

            self.after(20, self.OnStop)

    def takethephoto(self): #updates gui before taking photo
        self.after(50, self.take_photo) #takes photo after 50 milliseconds

    def take_photo(self):
        if(self.webcam.isOpened()):
            if self.updateB is True:
                self.message["text"] = "Status: Taking photo..."
                try:
                    timestamp = time.strftime("%m_%d_%y-%H%M%S")
                    _, frame = self.webcam.read()
                    success = cv2.imwrite("captures/cap%s.jpg" %timestamp, frame)
                    frame = cv2.flip(frame, 1)
                    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) # converts colors/image
                    self.img = im.fromarray(cv2image)
                    self.activateWebcam()
                    img_array = emotionRecognition.faceLocalization(self.img) #analyzes photo
                    self.message["text"] = "Status: Face detected."
                    imgtk = imTk.PhotoImage(image=self.img) # converts photo to Tk Image
                    self.webcamLbl.imgtk = imgtk
                    self.webcamLbl.configure(image=imgtk) # puts img into gui
                    self.photoTaken = True
                    self.emotion = emotionRecognition.retEmotion(img_array)  # gets emotion most likely found
                    self.message["text"] = "Status: Emotion analyzed."
                    self.emotionLabel["text"] = "Emotion: " + self.emotion
                    self.after(100, self.getSong)
                except:
                    self.message["text"] = "Status: Couldn't detect emotion."
            else:
                self.message["text"] = "Status: Webcam not active."
    
    def getSong(self): # plays the song from emotion string
        self.message["text"] = "Status: Looking for song"
        try: # catches exception so that gui doesn't freeze indefinitely
            audio = flAudio.facelistAudio() # init soundcloud library
            # neutral isn't a great keyword, so only use emotion if we didn't get neutral
            self.message["text"] = "Status: Searching SoundCloud."
            found = False
            if(self.curated.get() == 1):
                playlistUrl = audio.emotionToPlaylistURL(self.emotion.lower())
                found = audio.getPlaylist(playlistUrl)
            else:
                found = audio.getSong(self.emotion.lower())
            
            if found == True and audio.retSizeArr() > 0:
                tempVar = audio.getTrackInfo(audio.retSizeArr() - 1)
                tempVar["emotion"] = self.emotion
                tempVar = self.checkLengths(tempVar, 40)
                self.songs.append(tempVar)
                self.songCounter = len(self.songs)
                self.songURL = self.songs[len(self.songs)-1]["stream_url"]
                self.songName["text"] = "Song: " + self.songs[audio.retSizeArr()-1]["track_title"]
                self.artistName["text"] = "Artist: " + self.songs[audio.retSizeArr()-1]["track_artist"]["username"]
                self.emotionLabel["text"] = "Emotion: " + self.emotion
                #self.after(60, lambda: self.showURLImage(self.songs[len(self.songs)-1]["track_artwork"]))
                url = self.songs[len(self.songs)-1]["track_artwork"].replace("large","t500x500")
                self.showURLImage(url)
                self.message["text"] = "Status: Ready to play."
                if(len(self.songs) > 1):
                    self.prevButton["state"] = "normal"

            else:
                self.message["text"] = "Status: No song found."
        except:
            self.message["text"] = "Status: Couldn't find song."
            self.showImage("default.jpg")

    def updateFrame(self): # updates gui
        if self.updateB is True:
            self.updateCam()
            self.after(20, self.updateFrame)

    def showURLImage(self, url):
        try:
            fileArtwork = str(self.songCounter) + "_artwork.jpg"
            request.urlretrieve(url, "artwork/" + fileArtwork)
            self.showImage(fileArtwork)
        except:
            self.message["text"] = "Status: Error getting song artwork."

    def showImage(self, fileName):
        try:
            image = im.open("artwork/" + fileName) 
            image = image.resize((500,500), im.BILINEAR)
            photo = image
            imgtk = imTk.PhotoImage(image=image)
            self.webcamLbl.imgtk = imgtk 
            self.webcamLbl.configure(image=imgtk) # puts img into gui
        except:
            self.message["text"] = "Image not found."

    def activateWebcam(self):
        self.updateB = not self.updateB
        if self.updateB == True:
            self.webCamButton["text"] = "Webcam Active"
            self.shutter["state"] = "normal"
            self.after(100, self.updateFrame)
        else:
            self.webCamButton["text"] = "Webcam Idle"
            self.showImage("default.jpg")
            self.shutter["state"] = "disabled"
        
        
    def updateCam(self): #updates webcam feed
        _, frame = self.webcam.read() # reads from webcam
        frame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        self.img = im.fromarray(cv2image)
        imgtk = imTk.PhotoImage(image=self.img) #converts to proper image format
        self.webcamLbl.imgtk = imgtk 
        self.webcamLbl.configure(image=imgtk) # puts img into gui

    def OnExit(self, evt):
        """Closes the window.
        """
        self.Close()

    def OnOpen(self):
        """Pop up a new dialow window to choose a file, then play the selected file.
        """
        # if a file is already running, then stop it.
        self.OnStop()

        self.Media = self.Instance.media_new(self.songURL)
        self.lastURL = self.songURL
        self.Media.get_mrl()

        self.player.set_media(self.Media)
        self.player.play()

        # set the window id where to render VLC's video output
        if platform.system() == 'Windows':
            self.player.set_hwnd(self.GetHandle())
        else:
            self.player.set_xwindow(self.GetHandle()) # this line messes up windows

        # set the volume slider to the current volume
        #self.volslider.SetValue(self.player.audio_get_volume() / 2)
        #self.player.audio_set_volume(self.volume_var.get())
        #self.volslider.set(self.player.audio_get_volume())

    def OnPlay(self):
        """Toggle the status to Play/Pause.
        If no file is loaded, open the dialog window.
        """
        # check if there is a file to play, otherwise open a
        # Tk.FileDialog to select a file
        if(len(self.songs) > 0):

            if not self.player.get_media():
                self.OnOpen()
            else:
                if self.lastURL != self.songURL:
                    self.OnOpen()
                else:
                    # Try to launch the media, if this fails display an error message
                    if self.player.play() == -1:
                        self.errorDialog("Unable to play.")
        else:
            self.message["text"] = "Status: No song yet."

    def checkLengths(self, songInfo, lengthStr):
        if len(songInfo["track_title"]) > lengthStr:
            songInfo["track_title"] = songInfo["track_title"][0:lengthStr]
        if len(songInfo["track_artist"]["username"]) > lengthStr:
            songInfo["track_artist"]["username"] = songInfo["track_artist"]["username"][0:lengthStr]
        return songInfo

    def GetHandle(self):
        return self.videopanel.winfo_id()

    #def OnPause(self, evt):
    def OnPause(self):
        """Pause the player.
        """
        self.player.pause()

    def OnStop(self):
        """Stop the player.
        """
        self.player.stop()
        # reset the time slider
        self.timeslider.set(0)
    #start photostrip creation functions 
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
                filename = "photostrips/%s.jpg"%timestamp
            newImage.save(filename)
            savedImage = im.open(filename)
            savedImage.load()
            savedImage.show()

        else:
            self.initText = "CHOOSE 5 IMAGES (NO MORE OR LESS)."
            self.label.config(fg='red')
    def OnTimer(self):
        """Update the time slider according to the current movie time.
        """
        if self.player == None:
            return
        # since the self.player.get_length can change while playing,
        # re-set the timeslider to the correct range.
        length = self.player.get_length()
        dbl = length * 0.001
        self.timeslider.config(to=dbl)

        # update the time on the slider
        tyme = self.player.get_time()
        if tyme == -1:
            tyme = 0
        dbl = tyme * 0.001
        self.timeslider_last_val = ("%.0f" % dbl) + ".0"
        # don't want to programatically change slider while user is messing with it.
        # wait 2 seconds after user lets go of slider
        if time.time() > (self.timeslider_last_update + 2.0):
            self.timeslider.set(dbl)

    def scale_sel(self, evt):
        if self.player == None:
            return
        nval = self.scale_var.get()
        sval = str(nval)
        if self.timeslider_last_val != sval:
            # this is a hack. The timer updates the time slider.
            # This change causes this rtn (the 'slider has changed' rtn) to be invoked.
            # I can't tell the difference between when the user has manually moved the slider and when
            # the timer changed the slider. But when the user moves the slider tkinter only notifies
            # this rtn about once per second and when the slider has quit moving.
            # Also, the tkinter notification value has no fractional seconds.
            # The timer update rtn saves off the last update value (rounded to integer seconds) in timeslider_last_val
            # if the notification time (sval) is the same as the last saved time timeslider_last_val then
            # we know that this notification is due to the timer changing the slider.
            # otherwise the notification is due to the user changing the slider.
            # if the user is changing the slider then I have the timer routine wait for at least
            # 2 seconds before it starts updating the slider again (so the timer doesn't start fighting with the
            # user)
            self.timeslider_last_update = time.time()
            mval = "%.0f" % (nval * 1000)
            self.player.set_time(int(mval)) # expects milliseconds


    def volume_sel(self, evt):
        if self.player == None:
            return
        volume = self.volume_var.get()
        if volume > 100:
            volume = 100
        if self.player.audio_set_volume(volume) == -1:
            self.errorDialog("Failed to set volume")



    def OnToggleVolume(self, evt):
        """Mute/Unmute according to the audio button.
        """
        is_mute = self.player.audio_get_mute()

        self.player.audio_set_mute(not is_mute)
        # update the volume slider;
        # since vlc volume range is in [0, 200],
        # and our volume slider has range [0, 100], just divide by 2.
        self.volume_var.set(self.player.audio_get_volume())

    def OnSetVolume(self):
        """Set the volume according to the volume sider.
        """
        volume = self.volume_var.get()
        # vlc.MediaPlayer.audio_set_volume returns 0 if success, -1 otherwise
        if volume > 100:
            volume = 100
        if self.player.audio_set_volume(volume) == -1:
            self.errorDialog("Failed to set volume")

    def errorDialog(self, errormessage):
        """Display a simple error dialog.
        """
        #Tk.tkMessageBox.showerror(self, 'Error', errormessage)
        doNothing = 0

def Tk_get_root():
    if not hasattr(Tk_get_root, "root"): #(1)
        Tk_get_root.root= Tk.Tk()  #initialization call is inside the function
    return Tk_get_root.root

def _quit():
    print("_quit: bye")
    root = Tk_get_root()
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate
    os._exit(1)

if __name__ == "__main__":
    # Create a Tk.App(), which handles the windowing system event loop
    root = Tk_get_root()
    root.protocol("WM_DELETE_WINDOW", _quit)

    player = Player(root, title="FaceList")
    player.after(500, player.updateFrame)
    # show the player window centred and run the application
    root.mainloop()
