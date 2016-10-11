import soundcloud
import webbrowser
import sys
import time
import subprocess

client = soundcloud.Client(client_id="8c1cf28d0d2834808a2eda6645da717b", client_secret='67422b6c159a389c9cfed1a9607227ef', username='FaceList22@gmail.com',
                           password='Drawing76Drone')


page_size = 300

search = 'happy'

#search by happy tag
tracksList = client.get('/tracks', tags=search,  license='cc-by-sa', limit=2, streamable='true', embedable_by='all')
    
for track in tracksList:
    # get the tracks streaming URL
    stream_url = client.get(track.stream_url, allow_redirects=False)
    # print the tracks stream URL
    browser =subprocess.Popen(webbrowser.get().name, stream_url.location)
    time.sleep(track.duration/1000)
    browser.terminate()

    


    
