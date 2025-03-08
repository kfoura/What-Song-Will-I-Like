import numpy as np
from scipy.spatial.distance import cosine
import os

mfcc_list = []

# load in each of the MFCC arrays
for file in os.listdir("./dataset/normalized_mfcc_files"):
    if file.endswith(".npy"):
        mfcc = np.load(os.path.join('./dataset/normalized_mfcc_files', file))
        # take the average of each array
        mfcc_mean = np.mean(mfcc, axis=1)
        mfcc_list.append(mfcc_mean)

total_mfcc = np.mean(mfcc, axis=0)

new_file = "./dataset/new_mfcc.npy"
new_mfcc = np.load(new_file)
new_mfcc_mean = np.mean(new_mfcc, axis = 0)

similarities = []
for i, mfcc in enumerate(mfcc_list):
    similarity = 1 - cosine(mfcc, total_mfcc)
    similarities.append(similarity)

new_similarity = 1 - cosine(new_mfcc_mean, total_mfcc)

mean_similarites = np.mean(similarities)

if (new_similarity > mean_similarites):
    print("This song is sufficiently similar to the playlist.")