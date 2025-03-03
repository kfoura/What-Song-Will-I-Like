import spotipy
from spotipy.oauth2 import SpotifyOAuth

# # # # # # # # # # # # # # # # # # # # # # # 
# Not using this cuz spotify API fucked me  #   
# # # # # # # # # # # # # # # # # # # # # # # 

# Set up Spotify API credentials
client_id = "REMOVED"
client_secret = "REMOVED"
redirect_url = "http://localhost:3030"
scope = "user-library-read"


sp_oauth = SpotifyOAuth(client_id=client_id,
                         client_secret=client_secret,
                         redirect_uri=redirect_url,
                         scope=scope)
# Get the authorization URL
auth_url = sp_oauth.get_authorize_url()
print(f"Please go to this URL to authorize: {auth_url}")

# Get the authorization code from the user (after they log in and authorize)
#code = input("Enter the authorization code: ")

# Get the access token from the authorization code
token_info = sp_oauth.get_access_token("AQBYr_tfY-r1EqeXqB7lkuu8kHsv2P0X40AD660UuoIv_mN9Jm6skd8SSGtEFxL6luV1jhgAeGlsjrtTINBnX1hJ_ipUXIy4OVdHJAyZsoQsLWPbuQ6cUuWlz169E6fAr9_S5Z7RweKf8b6pof7Rl_Dy-Nisu6rfWkqMwa4W1ZWEio-4bEU06erV124")
access_token = token_info['access_token']

# Set up the Spotipy client with the access token
sp = spotipy.Spotify(auth=access_token)

# Get audio features of a song by its Spotify track ID
track_id = "3FYDqY5BRtx3IVSaiQZSze"  # Example song ID
track = sp.track(track_id)
print(track['preview_url'], track['name'])
