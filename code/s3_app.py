import streamlit as st
import boto3, os, s3fs
from zipfile import ZipFile

# Create connection object.
fs = s3fs.S3FileSystem(key = st.secrets["aws"]["aws_access_key_id"],
                        secret = st.secrets["aws"]["aws_secret_access_key"])

try:
    os.mkdir('downloads')
except OSError as error:
    # print(error)
    pass

st.set_page_config(page_title="S3 Music",page_icon="🎵")

@st.experimental_memo(ttl=600)
def read_file(filename):
    with fs.open(filename,"rb") as f:
        return f.read()

def write_local(filename,content):
    with open("downloads/"+filename,"wb") as f:
        f.write(content)

# l = fs.listdir("music48")
l = [i['Key'] for i in fs.listdir("music48")]
# l = [i.replace('music48/','') for i in fs.ls('music48')]
# st.write(l)
p = st.sidebar.selectbox("Select Playlist",l,format_func = lambda x : x.replace("music48/",""))
# st.sidebar.write(fs.listdir(p))
# st.sidebar.write(fs.isdir(p))

st.title("S3 Music 🎵")

d={}
b = st.checkbox("Select All")
st.write("---")

for i in fs.listdir(p):
    if i['type'] == "directory":
        st.write(i['Key'].replace(p,"")) 
        # TODO: add expander https://docs.streamlit.io/library/api-reference/layout/st.expander
        for j in fs.listdir(i['Key']):
            d[j['Key']] = st.checkbox(j['Key'].replace(i['Key']+"/",""),value=b)
            # st.write(j['Key'])
    elif i['type'] == "file":
        d[i['Key']] = st.checkbox(i['Key'].replace(p+"/",""),value=b)

# for i in fs.ls(p):
#     d[i] = st.checkbox(i,value=b)

# st.write(d)

# for key in d:
#     if d[key]:
#         st.write(key)

t = [key for key in d if d[key]]
# st.write(t)
z = ZipFile('downloads.zip', 'w')
for e in t:
    try:
        c = read_file(e)
        f = e.replace("music48/","").replace("/"," - ")
        # st.write(f)
        # st.audio(c)
        write_local(f,c)
        z.write('downloads/'+f)
    except: # avoid PermissionError: The operation is not valid for the object's storage class
        pass

z.close()

with open("downloads.zip", "rb") as fp:
    btn = st.download_button(
        label="Download ZIP",
        data=fp,
        file_name="music.zip",
        mime="application/zip"
    )