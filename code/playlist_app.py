import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from google.oauth2 import service_account
from gsheetsdb import connect
import os

clientId = st.secrets["clientId"]
clientSecret = st.secrets["clientSecret"]

# Setup

os.environ["SPOTIPY_CLIENT_ID"] = clientId
os.environ["SPOTIPY_CLIENT_SECRET"] = clientSecret
os.environ["SPOTIPY_REDIRECT_URI"] = "https://open.spotify.com/"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
# token  = spotifyAPI.get_token(clientId,clientSecret)


# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

# Playlist
sheet_url = st.secrets["private_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

st.title("Playlist")
# Print results.
for row in rows:
    track = sp.track(row.id)
    # st.write(track)
    st.write(track['name']+' - '+track['artists'][0]['name'])
    st.image(track['album']['images'][1]['url'], width=300)
    # st.write(f"{row.name} - {row.id}")