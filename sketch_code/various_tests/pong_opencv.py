import numpy as np
import cv2 as cv

radius = 10

frame_height = 512
frame_width = 1024

# display the frame in while loop
# place a circle that moves and bounce off the walls
# specify starting position and velocity
x = 5 + radius
y = 10 + radius
vx = 2
vy = 2

while True:
    # clear the frame
    frame = np.zeros((frame_height,frame_width,3), np.uint8)
    # draw a circle
    cv.circle(frame, (x,y), radius, (255,255,255), -1)
    # update the position
    x += vx
    y += vy
    # bounce off the walls
    if x < radius or x > frame_width - radius:
        vx = -vx
    if y < radius or y > frame_height - radius:
        vy = -vy
    # display the frame
    cv.imshow('frame', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()