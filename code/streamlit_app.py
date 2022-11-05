import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pytube
import moviepy.editor as mp
import os
from datetime import date, datetime, time, timedelta
import spotifyAPI
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from google.oauth2 import service_account
import gspread
import textwrap, random

# Setup Spotify

# from secret import *
clientId = st.secrets["clientId"]
clientSecret = st.secrets["clientSecret"]
os.environ["SPOTIPY_CLIENT_ID"] = clientId
os.environ["SPOTIPY_CLIENT_SECRET"] = clientSecret
os.environ["SPOTIPY_REDIRECT_URI"] = "https://open.spotify.com/"
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
token  = spotifyAPI.get_token(clientId,clientSecret)


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

# Getting All Values From a Worksheet as a Dataframe
d = worksheet.get_all_records()
df = pd.DataFrame(d)

def format_time(d):
    
    dt = datetime.combine(date.today(), time(0, 0)) + timedelta(seconds=d)
    return "%02d:%02d:%02d" % (dt.hour,dt.minute,dt.second)

@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

@st.cache
def random_song(df):
    s = df.sample()
    return s['name'].values[0]

try:
    os.mkdir('downloads')
except OSError as error:
    print(error)


mjstr = "🤘🎼🎵🎶 ♩♪♫♬♭♮♯ø 🎤🎸🎻🎷🎺📯🎹📻 🎧🎙🎚🎛📻📣📢🔊🔉🔈"
mjlist = textwrap.wrap(mjstr,width=1)
mj = random.choice(mjlist)
st.title("Music 48 "+mj)

# Sidebar

input = random_song(df)
search = st.sidebar.text_input('Enter Track',value=input)

results = sp.search(q=search,type='track')

track = results['tracks']['items'][0]
name = track['name']
album = track['album']['name']
artist = track['artists'][0]['name']
duration_ms = track['duration_ms']
popularity = track['popularity']
img_album = track['album']['images'][1]['url']
external_url = track['external_urls']['spotify']
track_id = track['id']

st.sidebar.image(img_album, caption=album,
        use_column_width=True)

display = st.selectbox('Display',('Song details','Recommendations','Playlist'))

if display == 'Song details':
    
    # Main song panel

    url = "https://open.spotify.com/track/"+str(track_id)
    st.write("Play: "+url)
    yt = st.button('Find on Youtube')

    if yt:
        try:
            
            r = pytube.Search(search).results
            # st.write(r[0].streams.first().title)
            # t = [i.streams.first().title for i in r]
            # st.radio("Search results",t)
            video = r[0].streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                
            # st.write(video)
            title = video.title
            path = video.download('downloads')
            st.markdown("["+title+"]("+video.url+")")
            # if st.checkbox('Show video'):
            #     st.video(path,format='video/mp4', start_time=0)

            # MoviePy processing
            my_clip = mp.VideoFileClip(path)
            duration = int(my_clip.duration)
            minutes, seconds = divmod(duration, 60)

            # Video to Audio
            my_clip.audio.write_audiofile("downloads/music.mp3")
            # st.text("Duration: "+format_time(duration))
            st.audio("downloads/music.mp3", format='audio/mp3')
            with open("downloads/music.mp3", "rb") as file:
                st.download_button("Download music",data=file,file_name=title+".mp3")
        except:
            st.write('Did not find the track on Youtube')
    
    ft = st.checkbox('Feature plot',value=True)

    if ft:     
        # Features polar plot 

        track_features = spotifyAPI.get_features(track_id,token)

        features = spotifyAPI.parse_features(track_features)

        # st.write(features)

        labels= list(features)[:]
        stats= features.mean().tolist()

        angles=np.linspace(0, 2*np.pi, len(labels), endpoint=False)

        # close the plot
        stats=np.concatenate((stats,[stats[0]]))
        angles=np.concatenate((angles,[angles[0]]))

        #Size of the figure
        fig=plt.figure(figsize = (18,18))
        ax = fig.add_subplot(221, polar=True)
        ax.plot(angles, stats, 'o-', linewidth=2, label = "Features", color= 'gray')
        ax.fill(angles, stats, alpha=0.25, facecolor='gray')
        ax.set_thetagrids(angles[0:7] * 180/np.pi, labels , fontsize = 13)
        ax.set_rlabel_position(250)
        plt.yticks([0.2 , 0.4 , 0.6 , 0.8  ], ["0.2",'0.4', "0.6", "0.8"], color="grey", size=12)
        plt.ylim(0,1)
        plt.legend(loc='best', bbox_to_anchor=(0.1, 0.1))

        st.pyplot(fig)

        if st.checkbox('What do those features mean?'):
            st.write("**acousticness**: Confidence measure from 0.0 to 1.0 on if a track is acoustic.")
            st.write("**danceability**: Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.")
            st.write("**energy**: Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.")
            st.write("**instrumentalness**: Predicts whether a track contains no vocals. “Ooh” and “aah” sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly “vocal”. The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.")
            st.write("**liveness**: Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.")
            st.write("**loudness**: The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typical range between -60 and 0 db.")
            st.write("**speechiness**: Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.")
            st.write("**tempo**: The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.")
            st.write("**valence**: A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).")

elif display == "Recommendations":
    
    # Central recommandation list

    json_response = spotifyAPI.get_track_reco(track_id,token)
    # st.write(json_response['tracks'][0])
    for i in json_response['tracks']:
        st.write('['+i['name']+' - '+i['artists'][0]['name']+']('+i['external_urls']['spotify']+')')
        # st.write(f"{i['name']} - {i['artists'][0]['name']}")
        st.image(i['album']['images'][1]['url'], width=300)


else:
    # Playlist

    # Append row
    if st.button("add to playlist"):
        worksheet.append_row([name,album,artist,duration_ms,popularity,img_album,external_url,track_id])

    # Getting All Values From a Worksheet as a Dataframe
    d = worksheet.get_all_records()
    df = pd.DataFrame(d)

    if st.checkbox("Playlist table"):
        
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

    for index,row in df[::-1].iterrows():
        # st.write(track)
        st.write('['+row['name']+' - '+row['artist']+']('+row['external_url']+')')
        st.image(row['img_album'], width=300)
