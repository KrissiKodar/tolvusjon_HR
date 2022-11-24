import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import sys

# capture video from camera
cap = cv.VideoCapture(1)

# when q is pressed, save the image, and exit

while(True):
    # Capture frame-by-frame
    try:
        ret, frame = cap.read()

        # Display the resulting frame
        cv.imshow('frame',frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            # save the last frame
            cv.imwrite('.\one_3.jpg', frame)
            break
    except:
        print('error')
