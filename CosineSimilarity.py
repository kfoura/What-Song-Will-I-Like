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