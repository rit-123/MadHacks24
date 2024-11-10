from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from collections import deque

class SpotifyActions:
    def __init__(self):
        self.access_token = None
        self.querier = None
        self.state = None
        self.songQ = deque()
    
    def setToken(self, token):
        self.access_token  = token
        self.querier = Spotify(self.access_token)


    def getSongs(self, query, mode, limit=10):
        if self.state == mode and self.isPlaying():
            return {"message":"same state"}
        results = self.querier.search(q=query, type='track', limit=limit)
        songs = []
        for item in results['tracks']['items']:
            song = {
                'name': item['name'],
                'artist': item['artists'][0]['name'],
                'album': item['album']['name'],
                'release_date': item['album']['release_date'],
                'uri': item['uri']
            }
            songs.append(song)
            self.songQ.append(song)
        self.playQueue()
        self.state = mode
        return songs

    def playQueue(self):
        songs = []
        while self.songQ:
            outSong = self.songQ.popleft()
            songURI = outSong["uri"]
            songs.append(songURI)
        self.querier.start_playback(uris=songs)

    def isPlaying(self):
        currState = self.querier.current_playback()
        return currState and currState["is_playing"]
