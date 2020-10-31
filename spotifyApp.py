import streamlit as st
# import pandas as pd
import spotifyAPI
from secrets import *
clientId = '5430345c1c6e472fae6e3fb2c1399bce'
clientSecret = 'ba32982d56ad4398834210941df54ccc'

token  = spotifyAPI.get_token(clientId,clientSecret)

st.title("Spotify Features App")

txt = st.text_input('Enter Track',value='Lucy in the Sky')

lucy_id = spotifyAPI.get_track_id2(txt, token)

url = "https://open.spotify.com/track/"+str(lucy_id)
# import webbrowser
# webbrowser.open(url)
st.write(url)

try:
    lucy_features = spotifyAPI.get_features(lucy_id,token)

    features = spotifyAPI.parse_features(lucy_features)

    # st.write(features)

    import numpy as np
    import matplotlib.pyplot as plt

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
except:
    st.write('Did not find the track on Spotify')

st.write("**acousticness**: Confidence measure from 0.0 to 1.0 on if a track is acoustic.")
st.write("**danceability**: Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.")
st.write("**energy**: Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.")
st.write("**instrumentalness**: Predicts whether a track contains no vocals. “Ooh” and “aah” sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly “vocal”. The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.")
st.write("**liveness**: Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.")
st.write("**loudness**: The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typical range between -60 and 0 db.")
st.write("**speechiness**: Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.")
st.write("**tempo**: The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.")
st.write("**valence**: A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).")


st.write("Information about features is from:  https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/")