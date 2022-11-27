import numpy as np
import cv2 as cv

# read frames from an ip camera

# cap = cv.VideoCapture("rtsp://[username]:[pass]@[ip address]/media/video1")

cap = cv.VideoCapture("rtsp://[username]:[pass]@14.160.87.118//media/video1")

while True:
    ret, frame = cap.read()
    cv.imshow('frame', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break