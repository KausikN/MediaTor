'''
Summary
Filter Functions
'''
import cv2
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# Basic Functions
def Correlation(I, W, stride=(1, 1)):
    I2 = I.copy().astype(float)
    W = W.copy()
    WSize = np.array(W.shape)
    if I.ndim == 2:
        I2 = np.reshape(I2, (I2.shape[0], I2.shape[1], 1))
    if WSize.shape[0] == 2:
        W = np.array([W]*I2.shape[2])

    padSize = (I2.shape[0] + 2*(W.shape[0]-1), I2.shape[1] + 2*(W.shape[1]-1), I2.shape[2])
    I_padded = np.zeros(padSize)
    I_padded[W.shape[0]-1:-W.shape[0]+1, W.shape[1]-1:-W.shape[1]+1, :] = I2[:, :, :]

    outSize = (int((I2.shape[0] + W.shape[0])/stride[0]), int((I2.shape[1] + W.shape[1])/stride[1]), I2.shape[2])
    I_g = np.zeros(outSize)
    print(I_g.shape)

    for i in tqdm(range(0, I_padded.shape[0]-W.shape[0]+1, stride[0])):
        for j in range(0, I_padded.shape[1]-W.shape[1]+1, stride[1]):
            for c in range(I_padded.shape[2]):
                I_g[i, j, c] = np.sum(np.sum(np.multiply(I_padded[i:i+W.shape[0], j:j+W.shape[1], c], W[:, :, c]), axis=1), axis=0)
            
    if I.ndim == 2:
        I_g = np.reshape(I_g, (I_g.shape[0], I_g.shape[1]))
    if WSize.shape[0] == 2:
        W = W[0]
    I_g = np.round(I_g).astype(np.uint8)
    return I_g

# Filter Generators
def GenerateEdgeFilter(size=(3, 3)):
    if size[0]%2 == 0 or size[1] == 0:
        return None
    W = np.ones(size) * -1
    W[int(size[0]/2), int(size[1]/2)] = -(size[0]*size[1] - 1)
    return W

def GenerateAverageFilter(size=(3, 3)):
    return np.ones(size).astype(float) / (size[0]*size[1])

# Filters
# Median Filter
def MedianFilter(I, WSize=(3, 3), stride=(1, 1)):
    I2 = I.copy()
    if I.ndim == 2:
        I2 = np.reshape(I2, (I2.shape[0], I2.shape[1], 1))

    padSize = (I2.shape[0] + 2*(WSize[0]-1), I2.shape[1] + 2*(WSize[1]-1), I2.shape[2])
    I_padded = np.zeros(padSize)
    I_padded[WSize[0]-1:-WSize[0]+1, WSize[1]-1:-WSize[1]+1, :] = I2[:, :, :]

    outSize = (int((I2.shape[0] + WSize[0])/stride[0]), int((I2.shape[1] + WSize[1])/stride[1]), I2.shape[2])
    I_g = np.zeros(outSize)

    for i in tqdm(range(0, I_padded.shape[0]-WSize[0]+1, stride[0])):
        for j in range(0, I_padded.shape[1]-WSize[1]+1, stride[1]):
            for c in range(I_padded.shape[2]):
                I_g[i, j, c] = np.median(I_padded[i:i+WSize[0], j:j+WSize[1], c])
            
    if I.ndim == 2:
        I_g = np.reshape(I_g, (I_g.shape[0], I_g.shape[1]))
    I_g = np.round(I_g).astype(np.uint8)
    return I_g

# Average Filtering
def AverageFilter(I, WSize=(3, 3)):
    return Correlation(I, GenerateAverageFilter(WSize))

# Special Filters

def DarkGreenSkinFilter(I):
    return cv2.cvtColor(I, cv2.COLOR_BGR2XYZ)

def BlueSkinFilter(I):
    return cv2.cvtColor(I, cv2.COLOR_BGRA2RGB)

def LSDBlueFilter(I):
    return cv2.cvtColor(I, cv2.COLOR_HLS2BGR)

def LSDRedFilter(I):
    return cv2.cvtColor(I, cv2.COLOR_HSV2BGR)

def LSDSoftBlueFilter(I):
    return cv2.cvtColor(I, cv2.COLOR_HLS2RGB)

def LSDSoftRedFilter(I):
    return cv2.cvtColor(I, cv2.COLOR_HSV2RGB)

def OrangeTintFilter(I):
    return cv2.cvtColor(I, cv2.COLOR_LUV2BGR)

def BlueTintFilter(I):
    return cv2.cvtColor(I, cv2.COLOR_LUV2RGB)

def Epic(I):
    return cv2.cvtColor(I, cv2.COLOR_RGB2HSV)