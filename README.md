# Spotify music recommendation [![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/slevin48/music/main/spotifyApp.py)

![feature-plot](spotifyData/features.svg)

This notebook leverages the Spotipy module to access the Spotify API:

https://spotipy.readthedocs.io/

* [Basic auth](basicMusic.ipynb)
  * Search & Get track
  * Get features
  * Get recommendations
* Spotipy auth
  * Artist albums
  * Artist top tracks
  * Advanced Search ([help](https://spotipy.readthedocs.io/en/2.16.1/#spotipy.client.Spotify.search))
  * Current user
* Access Scopes (detailed later)
  * Saved Tracks
  * Saved Albums ([doc](https://developer.spotify.com/console/get-current-user-saved-albums))
  * Playlist ([doc](https://developer.spotify.com/console/get-current-user-playlists/))
  * Recently played ([doc](https://developer.spotify.com/console/get-recently-played/))
  )
  * Advanced recommendations based on seeds ([doc](https://developer.spotify.com/console/get-recommendations/))

![spotifyNoneUserData](spotifyNonUserData.png)

## Scopes

* Images
  * [ugc-image-upload](https://developer.spotify.com/documentation/general/guides/scopes/#ugc-image-upload)
* Spotify Connect
  * [user-read-playback-state](https://developer.spotify.com/documentation/general/guides/scopes/#user-read-playback-state)
  * [user-modify-playback-state](https://developer.spotify.com/documentation/general/guides/scopes/#user-modify-playback-state)
  * [user-read-currently-playing](https://developer.spotify.com/documentation/general/guides/scopes/#user-read-currently-playing)
* Playback
  * [streaming](https://developer.spotify.com/documentation/general/guides/scopes/#streaming)
  * [app-remote-control](https://developer.spotify.com/documentation/general/guides/scopes/#app-remote-control)
* Users
  * [user-read-email](https://developer.spotify.com/documentation/general/guides/scopes/#user-read-email)
  * [user-read-private](https://developer.spotify.com/documentation/general/guides/scopes/#user-read-private)
* Playlists
  * [playlist-read-collaborative](https://developer.spotify.com/documentation/general/guides/scopes/#playlist-read-collaborative)
  * [playlist-modify-public](https://developer.spotify.com/documentation/general/guides/scopes/#playlist-modify-public)
  * [playlist-read-private](https://developer.spotify.com/documentation/general/guides/scopes/#playlist-read-private)
  * [playlist-modify-private](https://developer.spotify.com/documentation/general/guides/scopes/#playlist-modify-private)
* Library
  * [user-library-modify](https://developer.spotify.com/documentation/general/guides/scopes/#user-library-modify)
  * [user-library-read](https://developer.spotify.com/documentation/general/guides/scopes/#user-library-read)
* Listening History
  * [user-top-read](https://developer.spotify.com/documentation/general/guides/scopes/#user-top-read)
  * [user-read-playback-position](https://developer.spotify.com/documentation/general/guides/scopes/#user-read-playback-position)
  * [user-read-recently-played](https://developer.spotify.com/documentation/general/guides/scopes/#user-read-recently-played)
* Follow
  * [user-follow-read](https://developer.spotify.com/documentation/general/guides/scopes/#user-follow-read)
  * [user-follow-modify](https://developer.spotify.com/documentation/general/guides/scopes/#user-follow-modify)

## Parse Streaming History

Streaming history can be retrieved from the Spotify profile as JSON.

## Music Taste Analysis

Analysis of features to produce a polar plot

## Resources
* https://dev.to/mxdws/using-python-with-the-spotify-api-1d02
* https://medium.com/python-in-plain-english/music-recommendation-system-for-djs-d253d472677e
* https://github.com/tgel0/spotify-data
* https://towardsdatascience.com/a-visual-look-at-my-taste-in-music-a8c197a728be
* https://medium.com/@maxtingle/getting-started-with-spotifys-api-spotipy-197c3dc6353b
* https://towardsdatascience.com/a-music-taste-analysis-using-spotify-api-and-python-e52d186db5fc
* https://github.com/jmcabreira/A-Music-Taste-Analysis-Using-Spotify-API-and-Python.
* https://medium.com/analytics-vidhya/build-your-own-playlist-generator-with-spotifys-api-in-python-ceb883938ce4
* https://towardsdatascience.com/get-your-spotify-streaming-history-with-python-d5a208bbcbd3
* https://towardsdatascience.com/how-to-utilize-spotifys-api-and-create-a-user-interface-in-streamlit-5d8820db95d5
* https://developer.spotify.com/community/showcase/spotify-audio-analysis/
* https://medium.com/deep-learning-turkey/build-your-own-spotify-playlist-of-best-playlist-recommendations-fc9ebe92826a
* https://www.theverge.com/platform/amp/tldr/2018/2/5/16974194/spotify-recommendation-algorithm-playlist-hack-nelson
* http://sortyourmusic.playlistmachinery.com/
* https://towardsdatascience.com/k-means-clustering-and-pca-to-categorize-music-by-similar-audio-features-df09c93e8b64
* https://towardsdatascience.com/interactive-machine-learning-and-data-visualization-with-streamlit-7108c5032144
