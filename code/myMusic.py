import os, textwrap, random
import streamlit as st
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# --- allow HTTP on localhost (ONLY for dev) ---
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# --- load creds & scope from .streamlit/secrets.toml ---
cfg = st.secrets["spotify"]
sp_oauth = SpotifyOAuth(
    client_id=cfg["client_id"],
    client_secret=cfg["client_secret"],
    redirect_uri=cfg["redirect_uri"],
    scope=cfg["scope"],
    cache_path=None,        # no disk cache
    show_dialog=True,
)


st.set_page_config(page_title="My Music",page_icon="🎵",initial_sidebar_state="expanded")


mjstr = "🤘🎼🎵🎶 ♩♪♫♬♭♮♯ø 🎤🎸🎻🎷🎺📯🎹📻 🎧🎙🎚🎛📻📣📢🔊🔉🔈"
mjlist = textwrap.wrap(mjstr,width=1)
mj = random.choice(mjlist)
st.title("My Music "+mj)
st.write("*by Slevin48*")

# 1) First, check if Spotify just sent us back a code
if 'code' in st.query_params:
    token_info = sp_oauth.get_access_token(st.query_params["code"], as_dict=True)
    st.session_state.token_info = token_info
    st.query_params.clear()


# 2) If we still don’t have tokens in session, send them to login
if "token_info" not in st.session_state:
    auth_url = sp_oauth.get_authorize_url()
    # st.markdown(f"[👉 Authorize with Spotify]({auth_url})")
    st.link_button("👉 Authorize with Spotify", auth_url, type="primary")
    st.stop()

# 3) At this point we have token_info in session
token = st.session_state.token_info["access_token"]
sp = Spotify(auth=token)

# 4) Now you can make calls!
profile = sp.current_user()

with st.sidebar:
    st.write(f'Hello {profile['display_name']}')
    st.image(profile['images'][1]['url'])
    if st.toggle("debug"):
        st.write(st.session_state)
        st.json(profile)

st.subheader('Recently Played')

results = sp.current_user_recently_played(limit=50)
for idx, item in enumerate(results['items']):
    track = item['track']
    st.write(idx, track['artists'][0]['name'], " - ", track['name'])