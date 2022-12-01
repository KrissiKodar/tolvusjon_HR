import numpy as np
import cv2 as cv

cap = cv.VideoCapture(1)

radius = 10

frame_height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)
frame_width = cap.get(cv.CAP_PROP_FRAME_WIDTH)

# display the frame in while loop
# place a circle that moves and bounce off the walls
# specify starting position and velocity
x = 10 + radius
y = 10 + radius
vx = 1
vy = 1

font = cv.FONT_HERSHEY_SIMPLEX
average_fps = 0
e1 = cv.getTickCount()

# edge detection function, when edge of circle hits canny edge, change direction
def edge_detection(x, y, vx, vy):
    k = 0
    if x + radius >= frame_width:
        vx = -vx
        k += 1
    if x - radius <= 0:
        vx = -vx
        k += 1
    if y + radius >= frame_height:
        vy = -vy
        k += 1
    if y - radius <= 0:
        vy = -vy
        k += 1
    if k >= 1:
        print('edge of frame')
        return vx, vy
    # if vx and vy are positive then diagonal down right
    if vx > 0 and vy > 0:
        # check if bottom right corner of circle is on edge
        if edges[y + radius, x + radius] == 255:
            # change direction
            vx = -vx
            #vy = -vy
            return vx, vy
    # if vx is positive and vy is negative then diagonal up right
    elif vx > 0 and vy < 0:
        # check if top right corner of circle is on edge
        if edges[y - radius, x + radius] == 255:
            # change direction
            vx = -vx
            vy = -vy
            return vx, vy
    # if vx is negative and vy is positive then diagonal down left
    elif vx < 0 and vy > 0:
        # check if bottom left corner of circle is on edge
        if edges[y + radius, x - radius] == 255:
            # change direction
            vx = -vx
            vy = -vy
            return vx, vy
    # if vx and vy are negative then diagonal up left
    elif vx < 0 and vy < 0:
        # check if top left corner of circle is on edge
        if edges[y - radius, x - radius] == 255:
            # change direction
            vx = -vx
            vy = -vy
            return vx, vy
    # if vx is positive and vy is 0 then right
    elif vx > 0 and vy == 0:
        # check if right edge of circle is on edge
        if edges[y, x + radius] == 255:
            # change direction
            vx = -vx
            return vx, vy
    # if vx is negative and vy is 0 then left
    elif vx < 0 and vy == 0:
        # check if left edge of circle is on edge
        if edges[y, x - radius] == 255:
            # change direction
            vx = -vx
            return vx, vy
    return vx, vy


while True:
    # draw the circle on the video frame
    ret, frame = cap.read()
    # canny edge detection
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (5, 5), 0)
    edges = cv.Canny(gray, 100, 200)
    # draw a circle
    cv.circle(frame, (x,y), radius, (0,100,255), -1)
    # update the position
    x += vx
    y += vy
    # edge detection
    vx, vy = edge_detection(x, y, vx, vy)

    # also make the circle bounce off the edges
    # if the pixel value is 255, then bounce
    # if the pixel value is 0, then don't bounce
    # draw line though middle of edges that has a pixel value of 255
    # if the circle is on the line, then bounce
    cv.line(edges, (int(frame_width/2), 0), (int(frame_width/2), int(frame_height)), (255,255,255), 1)

    # display the frame
    # putting the FPS count on the frame
    time = (cv.getTickCount() - e1)/ cv.getTickFrequency()
    e1 = cv.getTickCount()
    fps = 1/time
    average_fps = average_fps + (fps - average_fps)/100
    cv.putText(frame, str(np.round(fps,1)), (10, 50), font, 1, (255, 255, 0), 2, cv.LINE_AA)
    cv.putText(frame, str(np.round(average_fps,1)), (10, 100), font, 1, (125, 0, 255), 2, cv.LINE_AA)
    cv.imshow('frame', frame)
    cv.imshow('edges', edges)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv.destroyAllWindows()