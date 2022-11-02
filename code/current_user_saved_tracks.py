import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

from secret import *
os.environ["SPOTIPY_CLIENT_ID"] = clientId
os.environ["SPOTIPY_CLIENT_SECRET"] = clientSecret
os.environ["SPOTIPY_REDIRECT_URI"] = "https://open.spotify.com/"

scope = "user-library-read"
username = '1146603936'

auth_user = SpotifyOAuth(scope=scope, username=username)
auth_user.get_cached_token()

sp = spotipy.Spotify(auth_manager=auth_user)

results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])