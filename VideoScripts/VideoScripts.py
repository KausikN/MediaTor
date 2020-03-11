'''
Summary
Script to access webcam and apply some basic filters
'''

import numpy as np
import cv2

import Filters as FilterFunctions

def DisplayVideo(videoPath=0, quitChar='q', Filters=None, FilterSizes=[], imgSize=(-1, -1)):
    cap = cv2.VideoCapture(videoPath)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        I = frame
        # I = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # If Filter apply it
        if not Filters == None:
            #I = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
            if not (imgSize[0] == -1 or imgSize[1] == -1):
                I = cv2.resize(I, imgSize, interpolation=cv2.INTER_LINEAR)
            for Filter, FilterSize in zip(Filters, FilterSizes):
                if not Filter == None:
                    if not (FilterSize[0] == -1 or FilterSize[1] == -1):
                        I = Filter(I, FilterSize)
                    else:
                        I = Filter(I)

        # Display the resulting frame
        cv2.imshow('Video', I)
        if cv2.waitKey(1) & 0xFF == ord(quitChar):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

def DisplayFilteredWebcamVideo(quitChar='q', Filters=None, FilterSizes=[], imgSize=(-1, -1)):
    DisplayVideo(0, quitChar=quitChar, Filters=Filters, FilterSizes=FilterSizes, imgSize=imgSize)

# Driver Code
Filters = [FilterFunctions.Epic]
FilterSizes = [(-1, -1)] * len(Filters)

DisplayFilteredWebcamVideo( Filters=Filters, 
                    FilterSizes=FilterSizes, 
                    imgSize=(-1, -1))