import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import sys


img = cv.imread('.\paper.jpg')


if img is None:
    sys.exit("Could not read the image.")

# canny edge detection
edges = cv.Canny(img, 190, 200)
lines = cv.HoughLines(edges, 1, np.pi / 90, 100)

# print how many lines are found
print(len(lines))
print(lines)
# draw lines on image
if lines is not None:
    for i in range(0, len(lines)):
        rho = lines[i][0][0]
        theta = lines[i][0][1]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
        pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
        cv.line(img, pt1, pt2, (0, 0, 255), 3, cv.LINE_AA)

# find intersection of lines, avoid duplicates, draw on image
intersect_of_lines = []
if lines is not None:
    try:
        for i in range(0, len(lines)):
            for j in range(i+1, len(lines)):
                rho1 = lines[i][0][0]
                theta1 = lines[i][0][1]
                rho2 = lines[j][0][0]
                theta2 = lines[j][0][1]
                # check if lines are near parallel, if so skip
                if abs(theta1 - theta2) < 0.6:
                    continue
                a = np.cos(theta1)
                b = np.sin(theta1)
                c = np.cos(theta2)
                d = np.sin(theta2)
                x = (d*rho1 - b*rho2) / (a*d - b*c)
                y = (a*rho2 - c*rho1) / (a*d - b*c)
                intersect_of_lines.append([x, y])
                cv.circle(img, (int(x), int(y)), 5, (0, 255, 0), -1)
    except:
        pass
print(intersect_of_lines)
print("len of intersect_of_lines: " + str(len(intersect_of_lines)))
print("size of image: " + str(img.shape))
#cv.circle(img, (551, 294), 5, (255, 0, 0), -1)
# pts src is a 4x2 array of the 4 corners of the rectangle 
pts_src = np.array([[intersect_of_lines[0][0], intersect_of_lines[0][1]], 
                    [intersect_of_lines[1][0], intersect_of_lines[1][1]], 
                    [intersect_of_lines[2][0], intersect_of_lines[2][1]],
                    [intersect_of_lines[3][0], intersect_of_lines[3][1]],])


#height and width in a4 paper ratio
ratio = 1.414
height = 400
width = int(height*ratio)
pts_dst = np.array([[0, 0], [0, width], [height, 0], [height, width]])

# sort points in pts_src
# plot pts_src with labels with scatter
plt.scatter(pts_src[:,0], pts_src[:,1])
for i in range(pts_src.shape[0]):
    plt.text(pts_src[i,0], pts_src[i,1], str(i))
# with axes like in opencv
plt.gca().invert_yaxis()
plt.show()

h, status = cv.findHomography(pts_src, pts_dst)
im_out = cv.warpPerspective(img, h, (height, width))

cv.imshow("Edges", edges)
cv.imshow("Source Image", img)
cv.imshow("Warped Source Image", im_out)

k = cv.waitKey(0)






""" # Read source image.q
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

print(img.shape) """