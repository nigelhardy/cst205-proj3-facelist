#! /usr/bin/python
# -*- coding: utf-8 -*-

#
# tkinter example for VLC Python bindings
# Copyright (C) 2015 the VideoLAN team
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston MA 02110-1301, USA.
#
"""A simple example for VLC python bindings using tkinter. Uses python 3.4

Author: Patrick Fay
Date: 23-09-2015
"""

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
else:
    import tkinter as Tk
    from tkinter import ttk
    from tkinter.filedialog import askopenfilename

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
songNames.append("Song Name:")
songNames.append("--NOT SET--")
songNames.append("Emotion:")
songNames.append("--NOT SET--")
songNames.append("Powered by SoundCloud")
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
        #self.actButton = Button() # activate webcam button
        self.webcamLbl = ttk.Label() # webcam image widget label
        self.photoTaken = False
        self.webcam = cv2.VideoCapture(0)
        self.img = self.webcam
        self.updateB = True # bool to start and stop webcam update
        self.lastURL = "EMPTY"
        #self.pack() # prepare gui
        self.speed = 10 # milliseconds between UI refresh
        self.counter = 0
        self.count = 0
        #self.createWidgets() # build gui
        self.c = 0
        self.numCount = 0
        self.songs = []
        self.songCounter = 0
        self.parent = parent

        if title == None:
            title = "tk_vlc"
        self.parent.title(title)

        # Menu Bar
        #   File Menu
        '''menubar = Tk.Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = Tk.Menu(menubar)
        fileMenu.add_command(label="Open", underline=0, command=self.OnOpen)
        fileMenu.add_command(label="Exit", underline=1, command=_quit)
        menubar.add_cascade(label="File", menu=fileMenu)
'''
        self.topPanel = ttk.Frame(self.parent)
        self.labelLeft = ttk.Label(self.topPanel, text="Label1")
        self.labelMiddle = ttk.Label(self.topPanel, text="Label2")
        self.labelRight = ttk.Label(self.topPanel, text="labelRight")
        webCamButton = ttk.Button(self.topPanel, text="Webcam", command=self.activateWebcam)
        shutter = ttk.Button(self.topPanel, text="Take Photo", command=self.takethephoto)
        playSongButton = ttk.Button(self.topPanel, text="Find Song", command=self.playSongSC)

        self.labelLeft.pack(side=Tk.LEFT)
        self.labelMiddle.pack(side=Tk.LEFT)
        self.labelRight.pack(side=Tk.LEFT)
        playSongButton.pack(side=Tk.RIGHT)
        shutter.pack(side=Tk.RIGHT)
        webCamButton.pack(side=Tk.RIGHT)
        
        
        self.topPanel.pack(fill=Tk.BOTH, expand=1)
        # The second panel holds controls
        self.player = None
        self.videopanel = ttk.Frame(self.parent)
        #self.canvas = Tk.Canvas(self.videopanel).pack(fill=Tk.BOTH,expand=1)
        image = im.open("your-image.jpg") 
        image = image.resize((300,300), im.BILINEAR)
        photo = image
        imgtk = imTk.PhotoImage(image=image)
        
        self.webcamLbl = ttk.Label(self.videopanel,image=imgtk, text="Stream")
        self.webcamLbl.image = imgtk
        self.webcamLbl.pack(side=Tk.BOTTOM)
        self.videopanel.pack(fill=Tk.BOTH,expand=1)

        ctrlpanel = ttk.Frame(self.parent)
        pause  = ttk.Button(ctrlpanel, text="Pause", command=self.OnPause)
        play   = ttk.Button(ctrlpanel, text="Play", command=self.OnPlay)
        stop   = ttk.Button(ctrlpanel, text="Stop", command=self.OnStop)
        #volume = ttk.Button(ctrlpanel, text="Volume", command=self.OnSetVolume)
        volume = ttk.Label(ctrlpanel, text="Volume")

        nextButton = ttk.Button(ctrlpanel, text="Next", command=self.OnNext)
        prevButton = ttk.Button(ctrlpanel, text="Previous", command=self.OnPrev)

        prevButton.pack(side=Tk.LEFT)
        pause.pack(side=Tk.LEFT)
        play.pack(side=Tk.LEFT)
        stop.pack(side=Tk.LEFT)
        nextButton.pack(side=Tk.LEFT)
        
        volume.pack(side=Tk.LEFT)

        self.volume_var = Tk.IntVar()
        self.volslider = Tk.Scale(ctrlpanel, variable=self.volume_var, command=self.volume_sel,
                from_=0, to=100, orient=Tk.HORIZONTAL, length=100)
        self.volslider.pack(side=Tk.LEFT)
        
        ctrlpanel.pack(side=Tk.BOTTOM)

        ctrlpanel2 = ttk.Frame(self.parent)
        self.scale_var = Tk.DoubleVar()
        self.timeslider_last_val = ""
        self.timeslider = Tk.Scale(ctrlpanel2, variable=self.scale_var, command=self.scale_sel,
                from_=0, to=1000, orient=Tk.HORIZONTAL, length=500)
        self.timeslider.pack(side=Tk.BOTTOM, fill=Tk.X,expand=1)
        
        self.timeslider_last_update = time.time()
        ctrlpanel2.pack(side=Tk.BOTTOM,fill=Tk.X)

        # VLC player controls
        self.Instance = vlc.Instance()
        self.player = self.Instance.media_player_new()

        # below is a test, now use the File->Open file menu
        #media = self.Instance.media_new('output.mp4')
        #self.player.set_media(media)
        #self.player.play() # hit the player button
        #self.player.video_set_deinterlace(str_to_bytes('yadif'))

        self.timer = ttkTimer(self.OnTimer, 1.0)
        self.timer.start()
        self.parent.update()

        #self.player.set_hwnd(self.GetHandle()) # for windows, OnOpen does does this
    def OnNext(self):
        
        if len(self.songs) > 0 and self.songCounter + 1 <= len(self.songs):
            self.songCounter += 1
            self.songURL = self.songs[self.songCounter-1]["stream_url"]
            self.labelRight["text"] = self.songs[self.songCounter-1]["stream_url"][6:30]
            self.labelMiddle["text"] = self.songs[self.songCounter-1]["track_title"]
            self.OnPlay()
        self.labelLeft["text"] = self.songCounter
    def OnPrev(self):
        self.labelLeft["text"] = self.songCounter
        if len(self.songs) > 0 and self.songCounter - 1 > 0:
            self.songCounter -= 1
            self.songURL = self.songs[self.songCounter-1]["stream_url"]
            self.labelRight["text"] = self.songs[self.songCounter-1]["stream_url"][6:30]
            self.labelMiddle["text"] = self.songs[self.songCounter-1]["track_title"]
            self.OnPlay()

        self.labelLeft["text"] = self.songCounter
    def takethephoto(self): #updates gui before taking photo
        songNames[4] = "Analyzing Photo..."
        #self.songLabels[4]["text"] = songNames[4]
        self.after(50, self.take_photo) #takes photo after 50 milliseconds

    def take_photo(self):
        if(self.webcam.isOpened()):
            if self.updateB is True:
                self.updateB = False
                _, frame = self.webcam.read()
                success = cv2.imwrite("cap%d.jpg"% self.count,frame) #saves photo
                self.count += 1
                frame = cv2.flip(frame, 1)
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) # converts colors/image
                self.img = im.fromarray(cv2image)
                img_array = emotionRecognition.faceLocalization(self.img) #analyzes photo
                imgtk = imTk.PhotoImage(image=self.img) # converts photo to Tk Image
                self.webcamLbl.imgtk = imgtk
                self.webcamLbl.configure(image=imgtk) # puts img into gui
                
                self.photoTaken = True
                songNames[3] = emotionRecognition.retEmotion(img_array)  # gets emotion most likely found
                self.labelRight["text"] = songNames[3]
                songNames[4] = "Photo has been taken."
        return imgtk
    def playSongSC(self): # plays the song from emotion string
        self.labelRight["text"] = "Looking for song"
        try: # catches exception so that gui doesn't freeze indefinitely
            audio = flAudio.facelistAudio() # init soundcloud library
            # neutral isn't a great keyword, so only use emotion if we didn't get neutral
            if songNames[3] != "Neutral":  
                audio.getSong(songNames[3].lower())    
            else:
                audio.getSong("relaxing") #used instead of neutral
            #songNames[1] = audio.getTrackTitle() 
            # updates gui to song name
            #self.songLabels[1]["text"] = songNames[1]
            #songNames[4] = "Found song."
            #self.songLabels[4]["text"] = songNames[4]
            if audio.retSizeArr() > 0:
                tempVar = audio.getTrackInfo(audio.retSizeArr() - 1)
                self.songs.append(tempVar)
                self.songCounter = audio.retSizeArr()
                self.songURL = self.songs[len(self.songs)-1]["stream_url"]
                self.labelRight["text"] = self.songs[audio.retSizeArr()-1]["stream_url"][8:30]
                self.labelMiddle["text"] = self.songs[audio.retSizeArr()-1]["track_title"]
                self.labelLeft["text"] = self.songs[audio.retSizeArr()-1]["track_artist"]["username"]
        except:
            self.labelRight["text"] = "Couldn't play song"
    def switchBool(self): # turns on and off the webcam feed
        self.updateB = not self.updateB
        if self.updateB is True:
            self.actButton["text"] = "Camera Activated"
            self.updateFrame()
        else:
            self.actButton["text"] = "Camera Deactivated"
    def updateFrame(self): # updates gui
        if self.updateB is True:
            #self.songLabels[0] = self.c
            #for s in songNames:
                #self.songLabels[self.count]["text"] = s
            self.updateCam()
            self.after(100, self.updateFrame)
    def activateWebcam(self):
        self.updateB = not self.updateB
        self.after(100, self.updateFrame)
        
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

        # Create a file dialog opened in the current home directory, where
        # you can display all kind of files, having as title "Choose a file".
        p = pathlib.Path(os.path.expanduser("~"))
        #fullname =  askopenfilename(initialdir = p, title = "choose your file",filetypes = (("all files","*.*"),("mp4 files","*.mp4")))
        #if os.path.isfile(fullname) or True:
            #dirname  = os.path.dirname(fullname)
            #filename = os.path.basename(fullname)
            # Creation
            #self.Media = self.Instance.media_new(str(os.path.join(dirname, filename)))
            #self.Media = self.Instance.media_new('https://cf-media.sndcdn.com/1hpt3bZE0l27.128.mp3?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiKjovL2NmLW1lZGlhLnNuZGNkbi5jb20vMWhwdDNiWkUwbDI3LjEyOC5tcDMiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE0NzkyODEwMzB9fX1dfQ__&Signature=NCAsX2V08EeVLi13cl9udAftjP0mXK9H6DYOiRDGJjCSoaPFNsAtJ7mnpnMGu7ShCFcEBqYc1yjsq9yxwQNQ9peN7SCAwni4AKkMay10thWFc-AUHBIYDAEmQIY3s2WJpx0yUY99ekO5maEz8r4IxKlG8TBUpC8LksaOqknRc3VmlIX1hJQoErjOt6C7QxIWnm~PGIYb5ZK2wzVNkxAV4pml3wZ~vAGH80cYFA42842VhoHCU~5Lzs8cEbh1hmbivHTElQ-5Q1QmHEoNTPFbE-BEaMVK0-ywsgIBkXk1RkEXlpz1u419EVxZ4jmLOUz32Zwm0~oaWCiOPkCsaXxyaw__&Key-Pair-Id=APKAJAGZ7VMH2PFPW6UQ')
            #self.songURL = 'https://cf-media.sndcdn.com/1hpt3bZE0l27.128.mp3?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiKjovL2NmLW1lZGlhLnNuZGNkbi5jb20vMWhwdDNiWkUwbDI3LjEyOC5tcDMiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE0NzkyODEwMzB9fX1dfQ__&Signature=NCAsX2V08EeVLi13cl9udAftjP0mXK9H6DYOiRDGJjCSoaPFNsAtJ7mnpnMGu7ShCFcEBqYc1yjsq9yxwQNQ9peN7SCAwni4AKkMay10thWFc-AUHBIYDAEmQIY3s2WJpx0yUY99ekO5maEz8r4IxKlG8TBUpC8LksaOqknRc3VmlIX1hJQoErjOt6C7QxIWnm~PGIYb5ZK2wzVNkxAV4pml3wZ~vAGH80cYFA42842VhoHCU~5Lzs8cEbh1hmbivHTElQ-5Q1QmHEoNTPFbE-BEaMVK0-ywsgIBkXk1RkEXlpz1u419EVxZ4jmLOUz32Zwm0~oaWCiOPkCsaXxyaw__&Key-Pair-Id=APKAJAGZ7VMH2PFPW6UQ'
        self.Media = self.Instance.media_new(self.songURL)
        self.lastURL = self.songURL
        self.Media.get_mrl()

        self.player.set_media(self.Media)
        self.player.play()
        # Report the title of the file chosen
        #title = self.player.get_title()
        #  if an error was encountred while retriving the title, then use
        #  filename
        #if title == -1:
        #    title = filename
        #self.SetTitle("%s - tkVLCplayer" % title)

        # set the window id where to render VLC's video output
        if platform.system() == 'Windows':
            self.player.set_hwnd(self.GetHandle())
        else:
            self.player.set_xwindow(self.GetHandle()) # this line messes up windows
        # FIXME: this should be made cross-platform

        # set the volume slider to the current volume
        #self.volslider.SetValue(self.player.audio_get_volume() / 2)
        self.volslider.set(self.player.audio_get_volume())

    def OnPlay(self):
        """Toggle the status to Play/Pause.
        If no file is loaded, open the dialog window.
        """
        # check if there is a file to play, otherwise open a
        # Tk.FileDialog to select a file
        if not self.player.get_media():
            self.OnOpen()
        else:
            if self.lastURL != self.songURL:
                self.OnOpen()
            else:
                # Try to launch the media, if this fails display an error message
                if self.player.play() == -1:
                    self.errorDialog("Unable to play.")

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
        Tk.tkMessageBox.showerror(self, 'Error', errormessage)

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
