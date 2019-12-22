'''
Summary
This project is to provide a set of tools for media viewing, manipulations and editing

'''

# Imports
from Image2Video import Img2Vid
# Imports

pathIn = input("Enter frames folder path: ") # './data/'
pathOut = input("Enter output video file path: ") # 'video.avi'
fps = float(input("Enter frames per second: ")) # 25.0
Img2Vid.convert_frames_to_video(pathIn, pathOut, fps)