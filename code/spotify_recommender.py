"""
spotify_recommender.py
======================
A minimal yet production‑ready script that:
1. Authenticates with Spotify via Spotipy & OAuth
2. Downloads every track in a chosen playlist (or your Liked Songs)
3. Normalises audio‑feature vectors
4. Trains a K‑Nearest‑Neighbours recommender in feature space
5. Spits out 5 fresh tracks similar to a chosen seed

How to run (🖥️ CLI):
====================
export SPOTIPY_CLIENT_ID="xxx"
export SPOTIPY_CLIENT_SECRET="yyy"
export SPOTIPY_REDIRECT_URI="http://localhost:8888/callback"
python spotify_recommender.py --playlist "37i9dQZF1DXcBWIGoYBM5M"  # Today's Top Hits
python spotify_recommender.py --playlist "spotify:playlist:37i9dQZF1DWSqBruwoIXkA" --track "3n3Ppam7vgaVa1iaRUc9Lp"

Copyright 2025  –  CC‑BY‑SA
"""

import os
import argparse
from typing import List

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import spotipy
from spotipy.oauth2 import SpotifyOAuth

###############
# 1. Auth
###############
SCOPE = "playlist-read-private user-library-read"

def auth_spotify() -> spotipy.Spotify:
    """OAuth dance using the three env vars declared above."""
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope=SCOPE,
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        )
    )

###############
# 2. Ingestion
###############

def fetch_playlist_tracks(sp: spotipy.Spotify, playlist_id: str) -> List[str]:
    """Return every track ID inside a playlist (handles pagination)."""
    track_ids = []
    results = sp.playlist_items(playlist_id, additional_types=["track"], limit=100)
    track_ids.extend([
        item["track"]["id"]
        for item in results["items"]
        if item.get("track") and item["track"].get("id")
    ])
    while results["next"]:
        results = sp.next(results)
        track_ids.extend([
            item["track"]["id"]
            for item in results["items"]
            if item.get("track") and item["track"].get("id")
        ])
    return track_ids

###############
# 3. Feature ETL
###############

def fetch_audio_features(sp: spotipy.Spotify, track_ids: List[str]) -> pd.DataFrame:
    """Download & normalise audio‑feature vectors for each track ID."""
    feats = []
    for i in range(0, len(track_ids), 50):  # Spotify max batch size = 100
        feats.extend(sp.audio_features(track_ids[i : i + 50]))
    df = pd.DataFrame(feats).set_index("id")
    numeric_cols = df.select_dtypes("number").columns
    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    return df

###############
# 4. Recommender
###############

def train_knn(df: pd.DataFrame, n_neighbors: int = 10) -> NearestNeighbors:
    model = NearestNeighbors(n_neighbors=n_neighbors, metric="cosine")
    model.fit(df.values)
    return model


def recommend(
    seed_id: str, df: pd.DataFrame, model: NearestNeighbors, k: int = 5
) -> List[str]:
    """Return K nearest track IDs to the seed (excluding itself)."""
    try:
        idx = df.index.get_loc(seed_id)
    except KeyError:
        raise ValueError("Seed track not found in dataframe – is it in the playlist?")
    dists, indices = model.kneighbors([df.iloc[idx].values], n_neighbors=k + 1)
    idxs = indices.flatten()[1:]  # drop the seed itself
    return df.index[idxs].tolist()

###############
# 5. CLI glue
###############

def cli():
    parser = argparse.ArgumentParser(description="Audio‑feature KNN recommender 🟢🎧")
    parser.add_argument("--playlist", required=True, help="Playlist URI or ID")
    parser.add_argument(
        "--track",
        help="Seed track URI/ID – default: first track in playlist",
        default=None,
    )
    parser.add_argument(
        "--k", type=int, default=5, help="Number of recommendations to return"
    )
    args = parser.parse_args()

    sp = auth_spotify()
    playlist_id = args.playlist.split(":")[-1]
    track_ids = fetch_playlist_tracks(sp, playlist_id)

    if not track_ids:
        raise SystemExit("⛔ Playlist appears empty – double‑check the ID/URI")

    df = fetch_audio_features(sp, track_ids)
    model = train_knn(df, n_neighbors=max(10, args.k + 1))

    seed_id = (args.track or track_ids[0]).split(":")[-1]
    rec_ids = recommend(seed_id, df, model, k=args.k)

    print("\nBecause you liked →", sp.track(seed_id)["name"], "\n")
    for uri in rec_ids:
        t = sp.track(uri)
        artists = ", ".join(a["name"] for a in t["artists"])
        print(f"- {t['name']} — {artists}")


if __name__ == "__main__":
    cli()
