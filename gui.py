#Author:  Nigel Hardy
#Created:  10/14/2016
#CSUMB CST-205 Project 3
#Team 40
#GitHub:  https://github.com/nigelhardy/cst205-proj3-facelist
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


def playSongSC(inputString): # plays the song from emotion string
        try: # catches exception so that gui doesn't freeze indefinitely
            audio = flAudio.facelistAudio() # init soundcloud library
            success = audio.getSong(inputString)
            return audio.getTrackInfo(audio.retSizeArr() - 1)
        except:
            print("Couldn't play song")
            return False
for x in range(0,10):
    temp = playSongSC("happy")
    if temp == False:
        print("Failed to find song.")
    else:
        print("Track: " + temp["track_title"])
        print("URL: " + temp["stream_url"])
        print("URL: " + temp["track_artwork"])
        print("Artist: " + temp["track_artist"]["username"])
