'''
Summary
This script is used for converting set of images to video
'''

# Imports
import numpy as np
import os

from cv2 import VideoWriter, imread, VideoWriter_fourcc
from os.path import isfile, join
# Imports

# Function
def convert_frames_to_video(pathIn, pathOut, fps=25.0, image_prefix=""):
    frame_array = []
    files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]
 
    print(files)
    
    for i in range(len(files)):
        filename = pathIn + files[i]
        # Read each image file
        img = imread(filename)
        height, width, layers = img.shape
        size = (width, height)
        print(filename)
        # Inserting the frames into an image array
        frame_array.append(img)
 
    out = VideoWriter(pathOut, VideoWriter_fourcc(*'DIVX'), fps, size)
 
    for i in range(len(frame_array)):
        # Writing to a image array
        out.write(frame_array[i])
    out.release()

