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

file = open('./dataset/songs.txt', 'r')

for line in file:
    search_query = line.strip()
    
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={search_query}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    video_id = data["items"][0]["id"]["videoId"]
    video_title = data["items"][0]["snippet"]["title"]
 
    video_url = f"https://www.youtube.com/watch?v={video_id}"



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

    file_path = f"{video_title} [{video_id}].mp3"




    # audio_stream = get_audio_stream(video_url)
    audio_data, sr = librosa.load(file_path, sr=None)
    #print(audio_data.shape, sr)
    tempo, _ = librosa.beat.beat_track(y=audio_data, sr=sr)


    mfccs = librosa.feature.mfcc(y=audio_data, sr=sr)
    mfcc = (mfccs - np.mean(mfccs)) / np.std(mfccs)  
    np.save(f"./dataset/normalized_mfcc_files/mfcc_{video_id}.npy", mfcc)
    os.remove(file_path)

file.close()
print("Success!")





# if I want to use a CNN model, use these graphs later
# plt.figure(figsize=(10, 6))
# librosa.display.specshow(mfccs, x_axis='time', sr=sr)

# plt.colorbar()
# plt.title("MFCCs of the track")
# plt.show()