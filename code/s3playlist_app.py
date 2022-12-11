import streamlit as st
import pandas as pd
import boto3, os
import os

try:
    os.mkdir('downloads')
except OSError as error:
    print(error)

s3_client = boto3.client('s3',aws_access_key_id = st.secrets["aws"]["aws_access_key_id"],
                    aws_secret_access_key = st.secrets["aws"]["aws_secret_access_key"])

s3_bucket = "music48"

st.set_page_config(page_title="S3 Playlist",page_icon="🎵")
st.title("S3 Music 🎵")

f = [key['Key'] for key in s3_client.list_objects(Bucket='music48',Prefix="Playlists/")['Contents']]

m = st.selectbox("Select Music",f,
            format_func = lambda x : x.replace("Playlists/","").replace(".csv",""))

if m != "Playlists/":
    object_name = m
    file_name = "downloads/"+m.replace("Playlists/","")+".csv"

    s3_client.download_file(s3_bucket, object_name,file_name)

    df = pd.read_csv(file_name,index_col=0)

    if st.checkbox("Playlist Table"):
        st.dataframe(df)

    for index,row in df[::-1].iterrows():
        st.write(row['name']+' - '+row['artist'])
        st.image(row['img_album'], width=300)