import os, textwrap, random, time, secrets
import streamlit as st
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth, SpotifyOauthError

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
st.set_page_config(page_title="My Music", page_icon="🎵", initial_sidebar_state="expanded")

cfg = st.secrets["spotify"]
sp_oauth = SpotifyOAuth(
    client_id=cfg["client_id"],
    client_secret=cfg["client_secret"],
    redirect_uri=cfg["redirect_uri"],   # MUST exactly match Spotify Dashboard
    scope=cfg["scope"],
    cache_path=None,
    show_dialog=True,
)

def save_token_info(token_info: dict):
    st.session_state.token_info = {
        "access_token": token_info["access_token"],
        "refresh_token": token_info.get("refresh_token"),
        "expires_at": token_info["expires_at"],
        "scope": token_info.get("scope"),
        "token_type": token_info.get("token_type", "Bearer"),
    }

def token_is_expired():
    ti = st.session_state.get("token_info")
    return not ti or time.time() > (ti["expires_at"] - 60)

def refresh_token_if_needed():
    ti = st.session_state.get("token_info")
    if ti and token_is_expired() and ti.get("refresh_token"):
        refreshed = sp_oauth.refresh_access_token(ti["refresh_token"])
        save_token_info(refreshed)

def get_sp():
    refresh_token_if_needed()
    ti = st.session_state.get("token_info")
    return Spotify(auth=ti["access_token"]) if ti else None

# ---------- UI header ----------
mj = random.choice(textwrap.wrap("🤘🎼🎵🎶 ♩♪♫♬♭♮♯ø 🎤🎸🎻🎷🎺📯🎹📻 🎧🎙🎚🎛📻📣📢🔊🔉🔈", width=1))
st.title(f"My Music {mj}")
st.write("*by Slevin48*")

qp = st.query_params

# Create a state for this session before showing login
if "code" not in qp and "oauth_state" not in st.session_state:
    st.session_state.oauth_state = secrets.token_urlsafe(32)

# ---------- Handle callback ----------
if "code" in qp:
    returned_state = qp.get("state")
    expected_state = st.session_state.get("oauth_state")

    # ★ If our session was rebuilt (no expected state), accept the returned state once and continue.
    if not expected_state and returned_state:
        st.session_state.oauth_state = returned_state  # ★ salvage the flow
        expected_state = returned_state

    # If still mismatch, ask to retry cleanly.
    if returned_state != expected_state:
        st.warning("OAuth state mismatch. Let's try again.")
        st.session_state.oauth_state = secrets.token_urlsafe(32)
        st.query_params.clear()
        st.link_button("👉 Re-authorize Spotify",
                       sp_oauth.get_authorize_url(state=st.session_state.oauth_state),
                       type="primary")
        st.stop()

    # Exchange code
    try:
        token_info = sp_oauth.get_access_token(qp["code"], as_dict=True)
        save_token_info(token_info)
        st.query_params.clear()  # avoid re-processing on refresh
    except SpotifyOauthError as e:
        st.error(f"Spotify OAuth error: {e}")
        st.stop()

# ---------- Not logged in? Prompt auth ----------
if "token_info" not in st.session_state:
    if "oauth_state" not in st.session_state:
        st.session_state.oauth_state = secrets.token_urlsafe(32)
    auth_url = sp_oauth.get_authorize_url(state=st.session_state.oauth_state)
    st.link_button("👉 Authorize with Spotify", auth_url, type="primary")
    st.stop()

# ---------- Have tokens; proceed ----------
sp = get_sp()
if sp is None:
    st.info("Session expired. Please re-authorize.")
    st.session_state.oauth_state = secrets.token_urlsafe(32)
    st.link_button("👉 Re-authorize Spotify",
                   sp_oauth.get_authorize_url(state=st.session_state.oauth_state),
                   type="primary")
    st.stop()

# === Your existing UI ===
profile = sp.current_user()
with st.sidebar:
    display_name = profile.get("display_name") or "Spotify user"
    st.write(f"Hello {display_name}")  # fixed quoting
    images = profile.get("images") or []
    if images:
        st.image(images[0]["url"], width=50)
    if st.button("🚪 Logout", type="secondary"):
        # clear session token(s)
        for k in ["token_info", "oauth_state"]:
            if k in st.session_state:
                del st.session_state[k]
        st.success("Logged out. Please re-authorize.")
        st.rerun()
    # if st.toggle("debug"):
    #     st.write(st.session_state)
    #     st.json(profile)

st.subheader("Recently Played")
results = sp.current_user_recently_played(limit=50)
items = results.get("items", [])
if not items:
    st.write("No recent tracks found (or scope missing).")
else:
    for idx, item in enumerate(items, start=1):
        track = item["track"]
        artists = ", ".join(a["name"] for a in track.get("artists", []))
        st.write(idx,f"{artists} — {track.get('name','')}")
