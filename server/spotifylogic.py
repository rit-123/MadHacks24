class SpotifyActions:
    def __init__(self):
        self.access_token = None

    def getSongs(self, query, limit=10):
        results = self.sp.search(q=query, type='track', limit=limit)
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
        return songs
