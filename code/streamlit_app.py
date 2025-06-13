import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pytubefix
import os
import boto3
import spotifyAPI
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import textwrap, random

st.set_page_config(page_title="Music 48",page_icon="🎵",initial_sidebar_state="expanded")

# Setup Spotify

# from secret import *
clientId = st.secrets["clientId"]
clientSecret = st.secrets["clientSecret"]
os.environ["SPOTIPY_CLIENT_ID"] = clientId
os.environ["SPOTIPY_CLIENT_SECRET"] = clientSecret
os.environ["SPOTIPY_REDIRECT_URI"] = "https://open.spotify.com/"
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
token  = spotifyAPI.get_token(clientId,clientSecret)


try:
    os.mkdir('downloads')
except OSError as error:
    print(error)


# Setup S3 

s3_client = boto3.client('s3',aws_access_key_id = st.secrets["aws"]["aws_access_key_id"],
                    aws_secret_access_key = st.secrets["aws"]["aws_secret_access_key"])

s3_bucket = "music48"
playlist = "playlist"
object_name = "Playlists/"+playlist+".csv"
file_name = "downloads/"+playlist+".csv"
s3_client.download_file(s3_bucket, object_name,file_name)

df = pd.read_csv(file_name,index_col=0)

@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')

@st.cache_data
def random_song(df):
    s = df.sample()
    return s['name'].values[0]

def update_params():
    st.query_params['song']=st.session_state.qp


if 'song' in st.query_params:
    song = st.query_params['song']
else:
    song = random_song(df)


mjstr = "🤘🎼🎵🎶 ♩♪♫♬♭♮♯ø 🎤🎸🎻🎷🎺📯🎹📻 🎧🎙🎚🎛📻📣📢🔊🔉🔈"
mjlist = textwrap.wrap(mjstr,width=1)
mj = random.choice(mjlist)
st.title("Music 48 "+mj)

# Sidebar

search = st.sidebar.text_input('Enter Track',value=song,key='qp',on_change=update_params)
st.query_params['song'] = search
try:
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

    st.sidebar.image(img_album, caption=album)

    display = st.selectbox('Display',('Song details','Recommendations','Playlist'))

    if display == 'Song details':
        
        # Main song panel

        url = "https://open.spotify.com/track/"+str(track_id)
        # st.markdown('![spoticon](../code/spoticon.png)')
        st.markdown('<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Spotify_icon.svg/232px-Spotify_icon.svg.png" width=20>Play: '+url,unsafe_allow_html=True)
        yt = st.button('Find on Youtube')

        if yt:
            try:
                
                r = pytubefix.Search(search).results
                # st.write(r[0].streams.first().title)
                # video = r[0].streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                video = r[0].streams.filter(only_audio=True).first()   
                # st.write(video)
                title = video.title
                out_file = video.download('downloads')
                st.markdown("["+title+"]("+video.url+")")
                # if st.checkbox('Show video'):
                #     st.video(path,format='video/mp4', start_time=0)

                # Video to Audio
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                if not os.path.exists(new_file):
                    os.rename(out_file, new_file)
                st.audio(new_file, format='audio/mp3')
                with open(new_file, "rb") as file:
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
            link = 'https://music48.streamlit.app/?song='+i['name'].replace(" ","+")
            spotlink = i['external_urls']['spotify']
            st.markdown('<a href="'+link+'" target="_self">'+i['name']+'</a>    <a href="'+spotlink+'"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Spotify_icon.svg/232px-Spotify_icon.svg.png" width=20></a>',unsafe_allow_html=True)
            # st.markdown('<a href="'+link+'" target="_self">'+i['name']+'</a> - <a href="'+spotlink+'">▶️</a>',unsafe_allow_html=True)
            # st.write('[▶️]('+i['external_urls']['spotify']+')')
            # st.write(f"{i['name']} - {i['artists'][0]['name']}")
            st.image(i['album']['images'][1]['url'], width=300)


    else:
        # Playlist
        pwd = st.sidebar.text_input("Playlist password")
        if pwd == st.secrets['playlist_pwd']:

            # Append row
            if st.button("add to playlist"):
                df2 = pd.Series([name,album,artist,duration_ms,popularity,img_album,external_url,track_id],
                        index=["name","album","artist","duration_ms","popularity","img_album","external_url","id"])
                # st.dataframe(df2)
                df = df.append(df2,ignore_index=True) # Deprecated
                # df = pd.concat([df,df2],ignore_index=True)
                df.to_csv(file_name)
                s3_client.upload_file(file_name, s3_bucket, object_name)
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
                link = 'https://music48.streamlit.app/?song='+row['name'].replace(" ","+")
                spotlink = row['external_url']
                st.markdown('<a href="'+link+'" target="_self">'+row['name']+'</a>   <a href="'+spotlink+'"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Spotify_icon.svg/232px-Spotify_icon.svg.png" width=20></a>',unsafe_allow_html=True)
                # st.markdown('<a href="'+link+'" target="_self">'+row['name']+'</a>',unsafe_allow_html=True)
                # st.markdown('[![spotify](../img/spoticon.png)]('+row['external_urls']['spotify']+')')
                st.image(row['img_album'], width=300)

except:
    st.write('Search not found')