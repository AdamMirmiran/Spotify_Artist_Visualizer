from lyricsgenius import Genius
import json
import re
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
import os

def regex_clean(lyrics):
    #Cleans lyrics data
    pattern = r'\[.*?\]'
    return re.sub(pattern, ' ', lyrics)

def get_lyrics(artist_name):
    #Gets Lyrics of Artist and generates wordcloud
    
    token = "RptOqRg1pFz_MBLHs9-5_8_wOkdDyHUdu5zhNSVzZllK8jRVNV--NT5KaW7NKJQj"
    genius = Genius(token, retries=5)
    #genius.verbose = False
    output = artist_name + 'lyrics.json'
    genius.search_artist(artist_name).save_lyrics(filename=output)

    with open(output) as json_data:
        data = json.load(json_data)
#
    df = pd.DataFrame(data['songs'])
    df.fillna('', inplace=True)
    df['lyrics'] = df['lyrics'].apply(regex_clean)
    text = " ".join(str(i) for i in df.lyrics)
    stopwords = set(STOPWORDS)
    #The Genius API produces strange 'LikeEmbed' text at the end which must be ignored.'
    stopwords.update('LikeEmbed', 'Lyrics', 'nan')
    wordcloud = WordCloud(width=800, height=400, stopwords=stopwords, background_color='white').generate(text)
    plt.figure( figsize=(20,10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    
    plt.tight_layout()
    plt.savefig('wordcloud'+ artist_name + '.png')
    os.remove(output)
    #plt.show()
    
