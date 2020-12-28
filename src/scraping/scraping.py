import requests
import urllib.parse as urlparse
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

base_url = 'https://www.uta-net.com/'
url_by_artist = 'https://www.uta-net.com/artist/2750/4/'
response = requests.get(url_by_artist)
soup = BeautifulSoup(response.text, 'lxml')
links = soup.find_all('td', class_='side td1')

    
def get_lyrics(url):
    time.sleep(1)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    
    song_title = soup.find('div', class_='title').get_text().replace('\n','')

    # 歌詞詳細ページ    
    song_lyrics = soup.find('div', itemprop='lyrics')
    song_lyric = song_lyrics.text
    song_lyric = song_lyric.replace('\n','')
    return song_title,song_lyric

def scraping(url_by_artist, f_path):
    df = pd.DataFrame()
    base_url = 'https://www.uta-net.com/'
    response = requests.get(url_by_artist)    
    soup = BeautifulSoup(response.text, 'lxml')
    links = soup.find_all('td', class_='side td1')
    titles = []
    lyrics = []
    for link in links:
        _url = urlparse.urljoin(base_url,link.a.get('href'))
        song_title,song_lyric = get_lyrics(_url)
        titles.append(song_title)
        lyrics.append(song_lyric)

    df['title'] = titles
    df['lyric'] = lyrics
    df.to_pickle(f_path)
    

def main():
    # yuming
    url_by_artist = 'https://www.uta-net.com/artist/2750/4/'
    f_path = '../../data/lyrics/m.matsutouya/lyrics.pkl'
    scraping(url_by_artist,f_path)

    # miyuki oneisama
    url_by_artist = 'https://www.uta-net.com/artist/3315/4/'
    f_path = '../../data/lyrics/m.nakajima/lyrics.pkl'
    scraping(url_by_artist,f_path)
    
main()    
