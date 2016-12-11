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
    #'audio component to FaceList project'

    #class variables
    tracks = [] #array of tracks
    track_info = [] #associative array of track information

    #constructor
    def __init__(self):
        self.client = soundcloud.Client(client_id="8c1cf28d0d2834808a2eda6645da717b", client_secret='67422b6c159a389c9cfed1a9607227ef')
    def retSizeArr(self):
        return len(self.tracks)

    #get a song based off of string passed in
    def getSong(self, search_str):
        self.emotion = search_str
        self.emotion = self.betterEmotion(self.emotion)
        print(self.emotion)
        count = 0
        limit = 100
        
        #search by happy tag
        try:
            tracksList = self.client.get('/tracks', tags=self.emotion, limit=limit, streamable='True')
            rand = random.randint(0,len(tracksList)-1)
            for track in tracksList:
                #get a random track from the list and add it to the list of tracks and list of durations
                if count is rand:
                    # get the tracks streaming URL
                    stream_url = self.client.get(track.stream_url, allow_redirects=False)
                    #assign relevant information to the track_info associative array
                    self.track_info = {"stream_url": stream_url.location, "track_title": track.title, "track_artist": track.user, "track_artwork": track.artwork_url}
                    #add the track to the array of track_info
                    self.tracks.append(self.track_info)
                count = count + 1
        except:
            return False
        if len(self.tracks) > 0:
            return True

    def getPlaylist(self, search_str):
        self.emotion = search_str
        count = 0
        limit = 100
        
        #search by happy tag
        try:
            playlist = self.client.get('/resolve', url=search_str)
            rand = random.randint(0,len(playlist.tracks)-1)
            #rand = 2
            for track in playlist.tracks:
                #print(track["user"])
                if(count == rand):
                    
                    trackFromPlaylist = self.client.get(track["stream_url"], allow_redirects=False)
                    #assign relevant information to the track_info associative array
                    self.track_info = {"stream_url": trackFromPlaylist.location, "track_title": track["title"], "track_artist": track["user"], "track_artwork": track["artwork_url"]}
                    #add the track to the array of track_info
                    self.tracks.append(self.track_info)
                count += 1
                #get a random track from the list and add it to the list of tracks and list of durations
        except:
            return False
        return True

    def emotionToPlaylistURL(self, emotionIn):
        if emotionIn == "happy":
            return 'https://soundcloud.com/ajake14/sets/good-energy-positive-energy'
        elif emotionIn == "sad":
            return 'https://soundcloud.com/freedskiers/sets/sad-sleep-songs'
        elif emotionIn == "angry":
            return 'https://soundcloud.com/thespacelord/sets/hard-rock-heavy-metal'
        elif emotionIn == "neutral" or emotionIn == "calm":
            return 'https://soundcloud.com/ichopi/sets/chill-ambient-hammock'
        elif emotionIn == "fear":
            return 'https://soundcloud.com/hardlee/sets/scary'
        elif emotionIn == "surprise":
            return 'https://soundcloud.com/max-miller-42/sets/bee-movie-soundtrack'
    #get the information of the track at the index provided
    def getTrackInfo(self, index):
        return self.tracks[index]
    def betterEmotion(self, emotionIn):
        happySyns = ["joyful","happy","upbeat","delight","ecstatic","thrilled","joy"]
        sadSyns = ["sad","bitter","down","somber","sorry","meloncholy","heartbroken","mourning","gloomy","grief","crying"]
        angrySyns = ["enraged","furious","irritable","outraged","angry","wrath","rage"]
        fearSyns = ["fear","terror","worry","horror","dread","panic","scared","fright","phobia"]
        surpiseSyns = ["awe","shock","wonder","unexpected","astounding"]
        neutralSyns = ["calm","chill","relaxing", "content"]
        emotionSyns = {}
        emotionSyns["happySyns"] = happySyns
        emotionSyns["sadSyns"] = sadSyns
        emotionSyns["angrySyns"] = angrySyns
        emotionSyns["fearSyns"] = fearSyns
        emotionSyns["surpriseSyns"] = surpiseSyns
        emotionSyns["calmSyns"] = neutralSyns
        return emotionSyns[emotionIn.lower() + "Syns"][random.randint(0, len(emotionSyns[emotionIn.lower() + "Syns"])-1)]
