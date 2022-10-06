import urllib.request
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import numpy as np
from PIL import Image, ImageDraw
import os
os.environ['SPOTIPY_CLIENT_ID'] = '28048a67d60e408cb1b6e2adff73add4'
os.environ['SPOTIPY_CLIENT_SECRET'] = '9f9843c3e1da490c903e8c8f5f3d9d06'
os.environ['SPOTIPY_REDIRECT_URI'] = 'https://localhost:8080/callback'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth())

def get_top_tracks(artist_ID, artist_name):
    results = sp.artist_top_tracks(artist_ID)
    str_output = '\033[4m' + artist_name + ' TOP TRACKS' + '\033[0m'
    str_output += "\n"
    for songs in results['tracks']:
        str_output += songs['name'] + '\n'
    return str_output