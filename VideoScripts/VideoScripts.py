'''
Summary
Script to access webcam and apply some basic filters
'''

import numpy as np
import cv2

def DisplayVideo(videoPath=0):
    cap = cv2.VideoCapture(videoPath)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        cv2.imshow('frame',gray)
        if cv2.waitKey(1) & 0xFF == ord(quitChar):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

def DisplayWebcamVideo(Filter=None, quitChar='q'):
    DisplayVideo(0)

# Driver Code
DisplayWebcamVideo()