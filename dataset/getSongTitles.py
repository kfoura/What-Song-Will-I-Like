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
                        redirect_uri='http://localhost:1111',
                        scope='user-library-read')

auth_url = sp_oauth.get_authorize_url()
print(f"Please go to this URL to authorize: {auth_url}")

auth_code = input("Enter auth code: ")

# Get the access token from auth code
token_info = sp_oauth.get_access_token(auth_code)
access_token = token_info['access_token']

file = open('songs.txt', 'w')
