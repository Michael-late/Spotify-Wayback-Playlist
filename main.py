from bs4 import BeautifulSoup
import requests
from html import unescape
from os import getenv
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd


load_dotenv()
user_key = getenv("client_id")
user_secret = getenv("client_secret")
my_uri = getenv("my_uri")

time = input("Which year do you want to travel to (YYYY-MM-DD)? ")
year = time.split("-")[0]
url = f"https://www.billboard.com/charts/hot-100/{time}/"
# url = f"https://www.billboard.com/charts/hot-100/2000-08-12"

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"}
response = requests.get(url,headers=header)
soup = BeautifulSoup(response.text,"html.parser")
titles = soup.select("li #title-of-a-story")
title = [unescape(x.getText(strip=True)) for x in titles]



sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=user_key,
                                               client_secret=user_secret,
                                               redirect_uri="https://example.com/",
                                               scope="playlist-modify-private",
                                               cache_path="cache.csv"))

username = sp.current_user()["id"]
print(username)
# result = sp.search(q=f"track: Blank Space year: 2014")["tracks"]["items"]
# print(result[0]["uri"])
# song_uri = pd.DataFrame.from_dict(result)["uri"][0]

year = 2000
song_uri_list = []
song_list = pd.DataFrame(title, columns=["Song Name"])

for name in title:
    try:
        query = f"track: {name} year: {year}"
        song_uri = sp.search(q=query)["tracks"]["items"][0]["uri"]
        song_uri_list.append(song_uri)
    except IndexError:
        pass
    
song_df = pd.DataFrame(list(zip(title,song_uri_list)),columns=["Song Name","Song URIs"])
print(song_df)

playlist = sp.user_playlist_create(username,f"{time} Billboard", public=False,description="Created using python")["id"]
sp.playlist_add_items(playlist_id=playlist,items=song_uri_list)