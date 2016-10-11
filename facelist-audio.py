import soundcloud

client = soundcloud.Client(client_id="8c1cf28d0d2834808a2eda6645da717b")


page_size = 50




















#rate limit is 15k per 24 hours

#creating a set

# create an array of track ids
tracks = map(lambda id: dict(id=id), [290, 291, 292])

# create the playlist
client.post('/playlists', playlist={
    'title': 'My new album',
    'sharing': 'public',
    'tracks': tracks
})


#adding tracks to a set

# create an array of track ids
tracks = map(lambda id: dict(id=id), [290, 291, 292])

# get playlist
playlist = client.get('/me/playlists')[0]

# add tracks to playlist
client.put(playlist.uri, playlist={
    'tracks': tracks
})


#accessing sets

# get playlist
playlist = client.get('/playlists/2050462')

# list tracks in playlist
for track in playlist.tracks:
    print track['title']


# searching for tracks

# find all sounds of buskers licensed under 'creative commons share alike'
tracks = client.get('/tracks', q='buskers', license='cc-by-sa')


# find all tracks with the genre 'punk' that have a tempo greater than 120 bpm.
tracks = client.get('/tracks', genres='punk', bpm={
    'from': 120
})


# iterating through the tracks

page_size = 100

# get first 100 tracks
tracks = client.get('/tracks', order='created_at', limit=page_size)
for track in tracks:
    print track.title

# start paging through results, 100 at a time
tracks = client.get('/tracks', order='created_at', limit=page_size,
                    linked_partitioning=1)
for track in tracks:
    print track.title


# getting track urls


# a permalink to a track
track_url = 'http://soundcloud.com/forss/voca-nomen-tuum'

# resolve track URL into track resource
track = client.get('/resolve', url=track_url)

# now that we have the track id, we can get a list of comments, for example
for track in client.get('/tracks/%d/comments' % track.id):
    print 'Someone said: %s at %d' % (comment.body, comment.timestamp)