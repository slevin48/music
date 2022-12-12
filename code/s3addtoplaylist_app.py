import streamlit as st
import pandas as pd
import boto3, os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Setup Spotify
clientId = st.secrets["clientId"]
clientSecret = st.secrets["clientSecret"]
os.environ["SPOTIPY_CLIENT_ID"] = clientId
os.environ["SPOTIPY_CLIENT_SECRET"] = clientSecret
os.environ["SPOTIPY_REDIRECT_URI"] = "https://open.spotify.com/"
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

try:
    os.mkdir('downloads')
except OSError as error:
    print(error)

s3_client = boto3.client('s3',aws_access_key_id = st.secrets["aws"]["aws_access_key_id"],
                    aws_secret_access_key = st.secrets["aws"]["aws_secret_access_key"])

s3_bucket = "music48"

st.set_page_config(page_title="S3 Add to Playlist",page_icon="🎵")
st.title("S3 Add to Playlist 🎵")

@st.cache
def read_playlist(file_name):
    return pd.read_csv(file_name,index_col=0)

# Sidebar

txt = st.sidebar.text_input("Enter Track","Lucy in the sky")
results = sp.search(q=txt,type='track')
# st.write(result)
track = results['tracks']['items'][0]
track_album = track['album']['name']
img_album = track['album']['images'][1]['url']
st.sidebar.image(img_album, caption=track_album)

# Main panel

f = [key['Key'] for key in s3_client.list_objects(Bucket='music48',Prefix="Playlists/")['Contents']]

m = st.selectbox("Select Music",f,
            format_func = lambda x : x.replace("Playlists/","").replace(".csv",""))

if m != "Playlists/":
    object_name = m
    file_name = "downloads/"+m.replace("Playlists/","")

    s3_client.download_file(s3_bucket, object_name,file_name)

    df = read_playlist(file_name)

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
        df2 = pd.Series([name,album,artist,duration_ms,popularity,img_album,external_url,track_id],
            index=["name","album","artist","duration_ms","popularity","img_album","external_url","id"])
        # st.dataframe(df2)
        df = df.append(df2,ignore_index=True) # Deprecated
        # df = pd.concat([df,df2],ignore_index=True)
        df.to_csv(file_name)
        s3_client.upload_file(file_name, s3_bucket, object_name)

    if st.checkbox("Playlist Table"):
        st.dataframe(df)

    for index,row in df[::-1].iterrows():
        st.write(row['name']+' - '+row['artist'])
        st.image(row['img_album'], width=300)