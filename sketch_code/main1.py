import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import sys


img = cv.imread('.\samples\data\home.jpg')


if img is None:
    sys.exit("Could not read the image.")

# Read source image.q
im_src = img
# Four corners of the book in source image
d=200
pts_src = np.array([[100+d, 100], [250+d, 200], [250+d, 250],[100+d, 300]])

# Four corners of the book in destination image.
r=700
t = 400
pts_dst = np.array([[0, 0], [t, 0], [t, t],[0, t]])

# Calculate Homography
h, status = cv.findHomography(pts_src, pts_dst)
#h = cv.getPerspectiveTransform(pts_src, pts_dst)

# Warp source image to destination based on homography
im_out = cv.warpPerspective(im_src, h, (t,t))
for i in range(pts_src.shape[0]):
    cv.circle(im_src, (pts_src[i,0],pts_src[i,1]), radius=5, color=(0, 0, 255),thickness=-1)
# Display images
cv.imshow("Source Image", im_src)
cv.imshow("Warped Source Image", im_out)

plt.show()

print(img.shape)


k = cv.waitKey(0)
