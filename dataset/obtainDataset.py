import requests
import yt_dlp
import librosa
import librosa.display  
import matplotlib.pyplot as plt
import numpy as np
from dotenv import load_dotenv, dotenv_values
import os
# matplot lib and librosa.display aren't strictly necessary

# get api key from hidden .env file
load_dotenv()
api_key = os.getenv('API_KEY')

# iterate through the songs.txt file to get each song
# TODO: add some way for a user to input their song or spotify account and they'll be able to check similarity with their own music tastes
file = open('./dataset/songs.txt', 'r')

for line in file:
    
    # remove whitespace, but if songs.txt is written correctly this shouldn't really be a problem
    search_query = line.strip()
    
    # searches youtube for the query
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={search_query}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    # parses and stores the video ID (aka what goes in the url of a youtube link) and the title of the song (for filename purposes)
    video_id = data["items"][0]["id"]["videoId"]
    video_title = data["items"][0]["snippet"]["title"]
 
    video_url = f"https://www.youtube.com/watch?v={video_id}"


    # use youtube downloader to download the mp3 file of the song
    ydl_opts = {
        'format': 'mp3/bestaudio/best',
        # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(video_url)

    # this is just how ydl titles the downloaded mp3s
    file_path = f"[{video_id}].mp3"



    # load the mp3 file into librosa
    
    audio_data, sr = librosa.load(file_path, sr=None)
    tempo, _ = librosa.beat.beat_track(y=audio_data, sr=sr)

    # calculate the mfcc values, then normalize them
    
    mfcc = librosa.feature.mfcc(y=audio_data, sr=sr)
    mfccNormalized = (mfcc - np.mean(mfcc)) / np.std(mfcc)  
    
    # save the arrays of mfcc values into a numpy array file
    
    np.save(f"./dataset/normalized_mfcc_files/mfcc_{video_id}.npy", mfccNormalized)
    
    # delete the mp3 file (if you have an ssd this doesn't do any damage to your storage, might cause defragmentation on hdds)
    os.remove(file_path)

# print a success message and close the file to avoid memory leaks
file.close()
print("Success!")





# if I want to use a CNN model, use these graphs later
# plt.figure(figsize=(10, 6))
# librosa.display.specshow(mfccs, x_axis='time', sr=sr)

# plt.colorbar()
# plt.title("MFCCs of the track")
# plt.show()