import streamlit as st
import boto3

s3_client = boto3.client('s3',aws_access_key_id = st.secrets["aws"]["aws_access_key_id"],
                    aws_secret_access_key = st.secrets["aws"]["aws_secret_access_key"])

def s3download(music):
    s3_client.download_file("music48", music, music)

st.set_page_config(page_title="S3 Music",page_icon="🎵")
st.title("S3 Music 🎵")

f = [key['Key'] for key in s3_client.list_objects(Bucket='music48',Prefix="downloads/")['Contents']]
m = st.selectbox("Select Music",f,
            format_func = lambda x : x.replace("downloads/","").replace(".mp3",""))

s3download(m)

st.audio(m)