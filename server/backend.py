from flask import Flask, request, redirect, jsonify, session
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotifylogic import SpotifyActions

app = Flask(__name__)

CLIENT_ID = '2486129522ca4ed8bf027362ebfd60b1'
CLIENT_SECRET = '76bd17dcb73548d49f7a45c22ab03c96'
REDIRECT_URI = 'http://127.0.0.1:5000/callback'

app.secret_key = 'your_secret_key_here'

sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,
                         client_secret=CLIENT_SECRET,
                         redirect_uri=REDIRECT_URI,
                         scope="user-read-private user-library-read")

spotifyObj = SpotifyActions()

@app.route('/')
def index():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    access_token = token_info['access_token']
    session["access_token"] = access_token
    spotifyObj.access_token = access_token
    return access_token

@app.route('/search', methods=["POST"])
def search():
    access_token = spotifyObj.access_token
    if not access_token:
        return jsonify({"error": "Access token missing or expired"}), 400

    body = request.get_json()
    query = body.get("query", "pop")

    sp = Spotify(auth=access_token)
    songs = getSongs(sp, query)

    return jsonify(songs)

def getSongs(sp, query, limit=10):
    results = sp.search(q=query, type='track', limit=limit)
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

if __name__ == "__main__":
    app.run(debug=True)
