#Author:  Brandon Avery
#Created:  10/12/2016
#CSUMB CST-205 Project 2
#Team 24
#GitHub:  https://github.com/nigelhardy/cst205-proj2-facelist

import soundcloud
import webbrowser
import sys
import time
import random 

class facelistAudio:
    'audio component to FaceList project'

    #class variables
    url_loc = []  #streaming url locations
    track_dur = [] #track durations
    track_title = [] #track titles
    
    

    #constructor
    def __init__(self):
        self.client = soundcloud.Client(client_id="8c1cf28d0d2834808a2eda6645da717b", client_secret='67422b6c159a389c9cfed1a9607227ef', username='FaceList22@gmail.com',
                           password='Drawing76Drone')
    def retSizeArr(self):
        return len(self.url_loc)

    #get a song based off of string passed in
    def getSong(self, search_str):
        count = 0
        rand = random.randint(0,19)
        #search by happy tag
        tracksList = self.client.get('/tracks', tags=search_str,  license='cc-by-sa', limit=20, streamable='true', embedable_by='all')
        for track in tracksList:
            # get the tracks streaming URL
            stream_url = self.client.get(track.stream_url, allow_redirects=False)
            #get a random track from the list and add it to the list of tracks and list of durations
            if count is rand:
                self.url_loc.append(stream_url.location)
                self.track_dur.append(track.duration/1000)
                self.track_title.append(track.title)
            count = count + 1

    #play the songs in the list
    def playSongs(self):
        for i in range(0,len(self.url_loc)):
            # open the tracks stream URL in a webbrowser
            browser = webbrowser.open(self.url_loc[i])
            # wait until the track is finished before opening the next track
            #time.sleep(self.track_dur[i])
            #time.sleep(1000)

    #return the array of track titles
    def getTrackTitle(self):
        titles = self.track_title[len(self.track_title)-1]
        return titles



    

