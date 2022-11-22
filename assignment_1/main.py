import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)

# hsv red
# lower boundary RED color range values; Hue (0 - 10)
lower1_red = np.array([0, 100, 20])
upper1_red = np.array([2, 255, 255])
 
# upper boundary RED color range values; Hue (160 - 180)
lower2_red = np.array([178,100,20])
upper2_red = np.array([180,255,255])

font = cv.FONT_HERSHEY_SIMPLEX
average_fps = 0
e1 = cv.getTickCount()

while(True):
    # for the double for loop
    """ max_value = 0
    maxLoc = (0,0) """
    ret, frame = cap.read()

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    minVal, maxVal, minLoc, maxLoc = cv.minMaxLoc(gray)
    
    # double for loop to find the max value of the gray image
    """ for i in range(gray.shape[0]):
        for j in range(gray.shape[1]):
            if gray[i,j] > max_value:
                max_value = gray[i,j]
                maxLoc = (i,j) """

    # find most red in hsv in frame
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask1 = cv.inRange(hsv, lower1_red, upper1_red)
    mask2 = cv.inRange(hsv, lower2_red, upper2_red)
    mask = mask1 + mask2
    res = cv.bitwise_and(frame, frame, mask=mask)
    # looking far maximum red saturation
    red_minVal, red_maxVal, red_minLoc, red_maxLoc = cv.minMaxLoc(res[:,:,1])
    
    # draw circle at brightest pixel
    cv.circle(frame, maxLoc, 10, (10, 210, 0), 2)
    # draw circle at most red pixel
    cv.circle(frame, red_maxLoc, 10, (0, 0, 255), 2)

    # putting the FPS count on the frame
    time = (cv.getTickCount() - e1)/ cv.getTickFrequency()
    e1 = cv.getTickCount()
    fps = 1/time
    average_fps = average_fps + (fps - average_fps)/100
    cv.putText(frame, str(np.round(fps,1)), (10, 50), font, 1, (255, 255, 0), 2, cv.LINE_AA)
    cv.putText(frame, str(np.round(average_fps,1)), (10, 100), font, 1, (125, 0, 255), 2, cv.LINE_AA)
    cv.imshow('frame',frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        # cv.imwrite('.\images\last_frame.jpg', frame)
        break

cap.release()
cv.destroyAllWindows()