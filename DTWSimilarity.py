# This algorithm uses DTW to compare MFCCs
import librosa
import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
import os

mfcc_list = []

# load in each of the MFCC arrays
for file in os.listdir('./dataset/normalized_mfcc_files'):
    if file.endswith('.npy'):
        mfcc = np.load(os.path.join('./dataset/normalized_mfcc_files', file))
        # take the average of each array
        mfcc_mean = np.mean(mfcc, axis=1)
        mfcc_list.append(mfcc_mean)
    
total_mfcc = np.mean(mfcc, axis = 0)

distance = []
for i, mfcc in enumerate(mfcc_list):
    # find the distance between the average MFCC and each MFCC
    dtw_distance = fastdtw(mfcc, total_mfcc, dist=euclidean)[0]
    distance.append(dtw_distance)
        
new_file = "./dataset/new_mfcc.npy"
new_mfcc = np.load(new_file)
new_mfcc_mean = np.mean(new_mfcc, axis = 1)
new_distance = fastdtw(new_mfcc, total_mfcc, dist=euclidean)[0]

distance_mean = np.mean(distance, axis=0)

if (new_distance <= distance_mean):
    print("This song is sufficiently similar to the playlist.")