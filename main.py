import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import pandas as pd
import matplotlib.pyplot as plt
import cv2
from Genius_API import *
from get_artist_logo import *
from Top_songs import get_top_tracks
from radar_plot import make_radar
from PIL import Image, ImageFont, ImageDraw
plt.style.use('ggplot')
import numpy as np
import sys

os.environ['SPOTIPY_CLIENT_ID'] = '28048a67d60e408cb1b6e2adff73add4'
os.environ['SPOTIPY_CLIENT_SECRET'] = '9f9843c3e1da490c903e8c8f5f3d9d06'
os.environ['SPOTIPY_REDIRECT_URI'] = 'https://localhost:8080/callback'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth())
#This can be obtained directly from the spotify URL
artist_ID = sys.argv[1]

#Input Artist ID
artist_name = sp.artist(artist_ID).get('name')
album_list = sp.artist_albums(artist_ID)
#print(album_list.get('items'))
album_IDs = []
song_names = []
#get the album IDs
for items in album_list.get('items'):
    album_IDs.append(items.get('id'))

#get tracks from each album
track_ids = []
for i in album_IDs:
    for track in sp.album_tracks(i).get('items'):
        artist_ids = [a.get('id') for a in track.get('artists')]
        if artist_ID in artist_ids:
            track_ids.append(track.get('id'))
            song_names.append(track.get('name'))

def get_features(track_ids):
    
    features_list = []
    for tracks in track_ids:
        feature = sp.audio_features(tracks=tracks)
        if feature[0] == None:
            pass
        else:  
            features_list += sp.audio_features(tracks=tracks)
    return features_list
    
def create_dataframe(features):
    
    df = pd.DataFrame(features)
    remove_cols = ['key', 'analysis_url', 'time_signature', 'track_href', 'mode', 'speechiness', 'instrumentalness', 'liveness', 'type',
                   'id', 'uri', 'loudness']
    df.drop(columns=remove_cols, inplace=True)
    df['tempo'] = (df['tempo'] - 40) / 160 #using 40 bpm as min and 200 as max
    df['duration_ms'] = (df['duration_ms'] - 60000) / 300000
    df.rename(columns={"duration_ms": "Length", "valence": "Happiness", "tempo" : "Tempo", "danceability": "Danceability" , 
                       "energy" : "Energy", "acousticness": "Acousticness"}, inplace=True)
    column_titles = ['Danceability', 'Energy', 'Tempo', 'Happiness', 'Length', 'Acousticness']
    df = df.reindex(columns=column_titles)

    df.loc['mean'] =  df.mean()
    #scaling for values >1. Change to 0.985 for visibility.
    if df.loc['mean'].max() > 0.985:
        scale = df.loc['mean'].max() / 0.985
        df.loc['mean'] / scale
    return df
features_list = get_features(track_ids)
df = create_dataframe(features_list)
make_radar(df, artist_name)
artist_logo(artist_name)
get_lyrics(artist_name, song_names)
top_tracks = get_top_tracks(artist_ID, artist_name)

def combine_images(artist_name):
    radar_image = Image.open('radar_plot' + artist_name + '.png')
    wordcloud_image = Image.open('wordcloud' + artist_name + '.png')
    artist_logo = Image.open(artist_name + 'logo.png')

    w1, h1 = radar_image.size
    w2, h2 = wordcloud_image.size
    w3, h3 = artist_logo.size
    radar_image = radar_image.resize((1488,960), Image.ANTIALIAS)
    wordcloud_image= wordcloud_image.resize((1500,750), Image.ANTIALIAS)
    artist_logo = artist_logo.resize((750,750), Image.ANTIALIAS)
    # to calculate size of new image 
    w = max(w1, w2, w3)
    h = max(h1, h2, h3)

    # create big empty image with place for images
    new_image = Image.new('RGB', (3250, h*2), color='grey')
    font_title = ImageFont.truetype("arial.ttf", 100)
    font_top = ImageFont.truetype("arial.ttf", 70)
    # put images on new_image
    new_image.paste(radar_image, (0,h))
    new_image.paste(wordcloud_image, (1250, h))
    new_image.paste(artist_logo, (0, 100))
    Text1 = ImageDraw.Draw(new_image)
    Text1.text((500,0), artist_name, font=font_title, fill =(255, 0, 0))
    Text2 = ImageDraw.Draw(new_image)
    Text2.text((1500,100), top_tracks, font=font_top, fill =(255, 0, 0))
    # save it
    new_image.save('new.png')
combine_images(artist_name)
    
