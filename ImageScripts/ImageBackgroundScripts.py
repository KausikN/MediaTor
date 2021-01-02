'''
Scripts related to image backgrounds
'''

# Imports
import cv2
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from skimage.morphology import skeletonize, thin

# Main Functions
def DisplayImage(I):
    plt.imshow(I)
    plt.show()

def SaveImage(I, path):
    print(I.shape)
    cv2.imwrite(path, I)

def Image_AddAlphaChannel(I, alphaValues):
    I_alpha = np.ones((I.shape[0], I.shape[1]), dtype=np.uint8) * alphaValues
    I_combined = np.zeros((I.shape[0], I.shape[1], 4), dtype=np.uint8)
    I_combined[:, :, :3] = I[:, :, :3]
    I_combined[:, :, 3] = I_alpha
    return I_combined

def ReadImage(path, imgSize=None):
    # Read Image and resize
    I = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if type(imgSize) == type(None) or (imgSize[0] == I.shape[0] and imgSize[1] == I.shape[1]):
        pass
    else:
        I = cv2.resize(I, imgSize)
    I = cv2.cvtColor(I, cv2.COLOR_BGR2RGBA)
    return I

def RemoveColours(I_alpha, colors):
    for i in tqdm(range(I_alpha.shape[0])):
        for j in range(I_alpha.shape[1]):
            for color in colors:
                if I_alpha[i, j, 0] == color[0] and I_alpha[i, j, 1] == color[1] and I_alpha[i, j, 2] == color[2]:
                    I_alpha[i, j, 3] = 0
                    break
    return I_alpha

def Image_Thin(I, iters=1):  
    I_thinned_alpha = (thin(np.greater_equal((I[:, :, 3]/255), 0.5), max_iter=iters)).astype(np.uint8)
    I_thinned = np.copy(I)
    I_thinned[:, :, 3] = I_thinned_alpha * 255
    return I_thinned

# Driver Code
# Params
path = 'MediaFiles/Disc_BGR.png'
imgSize = None

iters = 3

BackgroundColor = [0, 16, 255]
# Params

# RunCode
I = ReadImage(path, imgSize)

# Thin Image
I_thinned = Image_Thin(I, iters=iters)
DisplayImage(I_thinned)
I_thinned = cv2.cvtColor(I_thinned, cv2.COLOR_RGBA2BGRA)
SaveImage(I_thinned, 'MediaFiles/Disc_BGR_Thinned.png')
quit()

# Remove BG
I_alpha = Image_AddAlphaChannel(I, 255)

DisplayImage(I_alpha)

I_alpha_bgremoved = RemoveColours(I_alpha, [BackgroundColor])
DisplayImage(I_alpha_bgremoved)
I_alpha_bgremoved = cv2.cvtColor(I_alpha_bgremoved, cv2.COLOR_RGBA2BGRA)
SaveImage(I_alpha_bgremoved, 'MediaFiles/Disc_BGR.png')