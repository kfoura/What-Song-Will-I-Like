import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv, dotenv_values
import os

# Set up spotify API credentials
load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

sp_oauth = SpotifyOAuth(client_id=client_id, 
                        client_secret=client_secret,
                        redirect_uri='http://localhost:3030',
                        scope='user-library-read')

# Get the authorization URL
auth_url = sp_oauth.get_authorize_url()
print(f"Please go to this URL to authorize: {auth_url}")

auth_code = input("Enter auth code: ")

# Get the access token from auth code
token_info = sp_oauth.get_access_token(auth_code)
access_token = token_info['access_token']

# Set up the Spotipy client with the access token
sp = spotipy.Spotify(auth=access_token)

playlist_id = input("Please input the ID of the playlist you want to load in: ")
playlist = sp.playlist_items(playlist_id=playlist_id)



tracks = playlist['items']

# Pagination to get all tracks
while playlist['next']:
    playlist = sp.next(playlist)
    tracks.extend(playlist['items'])

file = open('./dataset/songs.txt', 'w', encoding = 'utf-8')

# Print track details
for idx, item in enumerate(tracks, start=1):
    track = item['track']
    file.write(f"{track['name']} - {track['artists'][0]['name']} \n")

file.close()