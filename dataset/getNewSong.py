import librosa
import requests
import numpy as np
import yt_dlp
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()
api_key = os.getenv("API_KEY")

song_name = input("Please enter the name of the song: ")
artist_name = input("Please enter the name of the artist: ")

search_query = f"{song_name} - {artist_name}"

url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={search_query}&key={api_key}"

response = requests.get(url)
data = response.json()

video_id = data["items"][0]["id"]["videoId"]
video_url = f"https://www.youtube.com/watch?v={video_id}"

ydl_opts = {
    'format': 'mp3/bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }]
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    error_code = ydl.download(video_url)

file_path = f"[{video_id}].mp3"

audio_data, sr = librosa.load(file_path, sr=None)

mfcc = librosa.feature.mfcc(y=audio_data, sr=sr)
mfccNormalized = (mfcc - np.mean(mfcc)) / np.std(mfcc)

np.save(f"./dataset/new_mfcc.npy")
os.remove(file_path)

print("Success!")
