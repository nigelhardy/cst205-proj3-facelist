import facelistAudio

audio = facelistAudio.facelistAudio()

audio.getSong('happy')
audio.getSong('anger')

print(audio.getTrackTitle())

audio.playSongs()

