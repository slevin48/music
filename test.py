import os
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotifyAPI

clientId = '5430345c1c6e472fae6e3fb2c1399bce'
clientSecret = 'ba32982d56ad4398834210941df54ccc'

os.environ["SPOTIPY_CLIENT_ID"] = clientId
os.environ["SPOTIPY_CLIENT_SECRET"] = clientSecret
os.environ["SPOTIPY_REDIRECT_URI"] = "https://open.spotify.com/"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
token  = spotifyAPI.get_token(clientId,clientSecret)

st.sidebar.title("Spotify Features App")
input = st.sidebar.empty()
txt = input.text_input('Enter Track',value='Lucy in the Sky')
track_id = sp.search(q='track:'+txt,type='track')['tracks']['items'][0]['id']

# input = st.empty()
# txt = input.text_input("Insert text:")
# bt = st.sidebar.button("Test")

json_response = spotifyAPI.get_track_reco(track_id,token)
bt = st.sidebar.button(json_response['tracks'][0]['name'])

if bt:
    txt = json_response['tracks'][0]['name']
    input.text_input('Enter Track', value=txt)


results = sp.search(q='track:'+txt,type='track')
st.sidebar.write(results['tracks']['items'][0]['name'])




