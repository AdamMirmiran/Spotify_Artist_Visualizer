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

def artist_logo(artist_name):
    #Downloads artist image from spotify URL 
    results = sp.search(q='artist:' + artist_name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        artist = items[0]
        image_url = artist['images'][0]['url']

    #Save artist logo as artist_namelogo.png
    urllib.request.urlretrieve(str(image_url), artist_name + "logo.png")
    img=Image.open(artist_name + "logo.png").convert("RGB")
    npImage=np.array(img)
    h,w=img.size

    # Create same size alpha layer with circle
    alpha = Image.new('L', img.size,0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0,0,h,w],0,360,fill=255)

    # Convert alpha Image to numpy array
    npAlpha=np.array(alpha)

    # Add alpha layer to RGB
    npImage=np.dstack((npImage,npAlpha))

    # Save with alpha
    Image.fromarray(npImage).save(artist_name + "logo.png")
