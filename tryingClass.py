class songClass(object):
    def __init__(self, name, url):
        self.songName = name
        self.songURL = url
sTemp = songClass("Song", "self.songURL")
songs = []

songs.append(sTemp)
print(songs[len(songs)-1].songURL)
