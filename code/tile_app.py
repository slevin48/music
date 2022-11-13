import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from google.oauth2 import service_account
import gspread
import os
import pandas as pd
from st_clickable_images import clickable_images

clientId = st.secrets["clientId"]
clientSecret = st.secrets["clientSecret"]

# Setup

os.environ["SPOTIPY_CLIENT_ID"] = clientId
os.environ["SPOTIPY_CLIENT_SECRET"] = clientSecret
os.environ["SPOTIPY_REDIRECT_URI"] = "https://open.spotify.com/"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
# token  = spotifyAPI.get_token(clientId,clientSecret)


# Setup Gspread

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
gc = gspread.authorize(credentials)

# Get playlist
sheet_url = st.secrets["private_gsheets_url"]
sh = gc.open_by_url(sheet_url)
worksheet = sh.sheet1

st.title("Playlist")
# Print results.

# Getting All Values From a Worksheet as a Dataframe
d = worksheet.get_all_records()
df = pd.DataFrame(d)

clicked = clickable_images(
df['img_album'].tolist(),
titles=[f"Image #{str(i)}" for i in range(df.size)],
div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
img_style={"margin": "5px", "height": "200px"}
)
st.markdown(f"Image #{clicked} clicked" if clicked > -1 else "No image clicked")