import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from google.oauth2 import service_account
import gspread
import os
import pandas as pd

# Setup Spotify
clientId = st.secrets["clientId"]
clientSecret = st.secrets["clientSecret"]
os.environ["SPOTIPY_CLIENT_ID"] = clientId
os.environ["SPOTIPY_CLIENT_SECRET"] = clientSecret
os.environ["SPOTIPY_REDIRECT_URI"] = "https://open.spotify.com/"
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())


# Setup Gspread
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
gc = gspread.authorize(credentials)


# Sidebar

txt = st.sidebar.text_input("Enter Track","Lucy in the sky")
results = sp.search(q=txt,type='track')
# st.write(result)
track = results['tracks']['items'][0]
track_album = track['album']['name']
img_album = track['album']['images'][1]['url']
st.sidebar.image(img_album, caption=track_album)
# st.sidebar.write(track['name'])
# st.write(track)
# st.sidebar.write(track['name']+' - '+track['artists'][0]['name'])


# Playlist
sheet_url = st.secrets["private_gsheets_url"]
sh = gc.open_by_url(sheet_url)
worksheet = sh.sheet1

st.title("Playlist")
# Print results

# Append row
name = track['name']
album = track['album']['name']
artist = track['artists'][0]['name']
duration_ms = track['duration_ms']
popularity = track['popularity']
img_album = track['album']['images'][1]['url']
external_url = track['external_urls']['spotify']
track_id = track['id']

if st.button("add to playlist"):
    worksheet.append_row([name,album,artist,duration_ms,popularity,img_album,external_url,track_id])


# # Getting a Cell Value
# val = worksheet.cell(1, 2).value
# st.write(val)

# # Get all values from the first row:
# values_list = worksheet.row_values(1)
# st.write(values_list)

# # Getting All Values From a Worksheet as a List of Lists
# list_of_lists = worksheet.get_all_values()
# st.write(list_of_lists)

# # Getting All Values From a Worksheet as a List of Dictionaries
# list_of_dicts = worksheet.get_all_records()
# st.write(list_of_dicts)

# Getting All Values From a Worksheet as a Dataframe
d = worksheet.get_all_records()
df = pd.DataFrame(d)

if st.checkbox("Playlist table"):
    @st.cache
    def convert_df(df):
        return df.to_csv().encode('utf-8')
    # st.table(df)
    st.dataframe(df)
        
    csv = convert_df(df)

    st.download_button(
    "download",
    csv,
    "playlist.csv",
    "text/csv",
    key='download-csv'
    )

for index,row in df.iterrows():
    # st.write(track)
    st.write(row['name']+' - '+row['artist'])
    st.image(row['img_album'], width=300)
