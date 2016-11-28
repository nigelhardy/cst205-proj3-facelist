#Author:  Brandon Avery
#Created:  10/14/2016
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
    tracks = [] #array of tracks
    track_info = [] #associative array of track information
    emotion = "blank"
    
    

    #constructor
    def __init__(self):
        self.client = soundcloud.Client(client_id="8c1cf28d0d2834808a2eda6645da717b", client_secret='67422b6c159a389c9cfed1a9607227ef', username='FaceList22@gmail.com',
                           password='Drawing76Drone')
    def retSizeArr(self):
        return len(self.url_loc)

    #get a song based off of string passed in
    def getSong(self, search_str):
        emotion = search_str
        count = 0
        rand = random.randint(0,19)
        #search by happy tag
        tracksList = self.client.get('/tracks', tags=search_str,  license='cc-by-sa', limit=20, streamable='true', embedable_by='all')
        for track in tracksList:
            
            #get a random track from the list and add it to the list of tracks and list of durations
            if count is rand:
                # get the tracks streaming URL
                stream_url = self.client.get(track.stream_url, allow_redirects=False)
                #assign relevant information to the track_info associative array
                self.track_info = {"stream_url": stream_url.location, "track_title": track.title, "track_artist": track.user, "track_artwork": track.artwork_url, "emotion": self.emotion}
                #add the track to the array of track_info
                self.tracks.append(self.track_info)
                self.emotion = "blank"
            count = count + 1

    #get the information of the track at the index provided
    def getTrackInfo(self, index):
        return self.tracks[index]
