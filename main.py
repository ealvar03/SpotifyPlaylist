from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Client ID
SPOTIPY_CLIENT_ID = "CLIENT ID"
# Client Secret
SPOTIPY_CLIENT_SECRET = "CLIENT SECRET"
URI = "http://example.com"

date = input("What year would you like to travel to? Type the date in this format:"
             "YYYY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/{date}"

response = requests.get(URL)
web_billboard = response.text

# Create a BeautifulSoup object
soup = BeautifulSoup(web_billboard, "html.parser")
songs_tag = soup.select("li ul li h3")

# Create a list with the 100 top songs on the date selected
top_songs = [item.getText().replace("\n", "").replace("\t", "") for item in songs_tag]

scope = "user-modify-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=URI, scope=scope, show_dialog=True, cache_path='token.txt'))
user_id = sp.current_user()["id"]
# Search for the songs in Spotify, if it does not exist then retrieve an exception message
uri_songs = []
year_song = date.split("-")[0]
for song in top_songs:
    result = sp.search(q=f"track: {song}, year: {year_song}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        uri_songs.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# Create a private playlist and add to it the songs on the date selected
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
billboard_playlist = sp.playlist_add_items(playlist_id=playlist["id"], items=uri_songs)