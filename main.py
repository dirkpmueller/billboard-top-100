from pprint import pprint
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

Client_ID = ""
Client_Secret = ""

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:\n")
URL = f"https://www.billboard.com/charts/hot-100/{date}"
print(URL)

response = requests.get(url=URL)

soup = BeautifulSoup(response.text, 'html.parser')
songs = soup.find_all("h3", class_="a-no-trucate")
title_list = [(song.getText().strip('\t\n')) for song in songs]
print(title_list)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=Client_ID,
        client_secret=Client_Secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

song_uris = []
year = date.split("-")[0]
for song in title_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # pprint(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

print(song_uris)

playlist = sp.user_playlist_create(user_id, name=f"{date} Billboard 100", public=False, collaborative=False, description=f"Billboard Top 100 from {date}")

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)