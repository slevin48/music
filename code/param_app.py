import streamlit as st
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Setup Spotify
clientId = st.secrets["clientId"]
clientSecret = st.secrets["clientSecret"]
os.environ["SPOTIPY_CLIENT_ID"] = clientId
os.environ["SPOTIPY_CLIENT_SECRET"] = clientSecret
os.environ["SPOTIPY_REDIRECT_URI"] = "https://open.spotify.com/"
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

st.title('Param app')


#When loading page with param
try:
    param = st.experimental_get_query_params()
    song = param['song'][0]
    search = st.text_input('Enter Track',value=song)
    st.experimental_set_query_params(song = search)

except: # catch exception and set query param to predefined value
    st.experimental_set_query_params(song = "Lucy in the Sky")
    param = st.experimental_get_query_params()
    song = param['song'][0]
    search = st.text_input('Enter Track',value=song)
    st.experimental_set_query_params(song = search)


st.write(param)
results = sp.search(q=search,type='track')


# Display image
track = results['tracks']['items'][0]
name = track['name']
album = track['album']['name']
artist = track['artists'][0]['name']
duration_ms = track['duration_ms']
popularity = track['popularity']
img_album = track['album']['images'][1]['url']
external_url = track['external_urls']['spotify']
track_id = track['id']

st.image(img_album, caption=album,
        use_column_width=True)
