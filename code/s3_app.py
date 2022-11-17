import streamlit as st
import boto3

s3_client = boto3.client('s3',aws_access_key_id = st.secrets["aws"]["aws_access_key_id"],
                    aws_secret_access_key = st.secrets["aws"]["aws_secret_access_key"])

def s3download(music):
    s3_client.download_file("music48", music, music)

st.set_page_config(page_title="S3 Music",page_icon="🎵")
st.title("S3 Music 🎵")

s3 = boto3.resource('s3')
bucket48 = s3.Bucket('music48')

f = [file.key for file in bucket48.objects.filter(Prefix="downloads/").all()]
m = st.selectbox("Select Music",f,
            format_func = lambda x : x.replace("downloads/","").replace(".mp3",""))

s3download(m)

st.audio(m)