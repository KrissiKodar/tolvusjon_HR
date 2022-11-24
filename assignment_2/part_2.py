import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import warnings

# turn off warnings
warnings.filterwarnings("ignore")
# capture video from camera
cap = cv.VideoCapture(0)

font = cv.FONT_HERSHEY_SIMPLEX
average_fps = 0
e1 = cv.getTickCount()

intersect_of_lines = []

#height and width in a4 paper ratio
ratio = 1.414
height = 400
width = int(height*ratio)

im_out = np.zeros((height, width, 3), np.uint8)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # reduce size of input image
    #frame = cv.resize(frame, (0,0), fx=0.5, fy=0.5)
    # convert to grayscale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # reduce noise with gaussian filter
    gray = cv.GaussianBlur(gray, (5, 5), 0)

    # Canny edge detection
    edges = cv.Canny(gray, 150, 200)

    # detect lines using hough transform, up to max 4 lines
    lines = cv.HoughLines(edges, 1, np.pi / 90, 100)
    
    
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
            cv.line(frame, pt1, pt2, (0, 0, 255), 3, cv.LINE_AA)

    # find intersection of lines and draw on image
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
                    # only append if intersection is within image frame
                    if x > 0 and x < frame.shape[1] and y > 0 and y < frame.shape[0]:
                        intersect_of_lines.append([x, y])
                        cv.circle(frame, (int(x), int(y)), 5, (0, 255, 0), -1)
        except:
            pass
    
    # print amount of lines detected
    # if lines is none do not print
    if lines is not None:
        print("Lines detected: " + str(len(lines)))
        print("intersections: " + str(len(intersect_of_lines)) + "\n")
    

    # Do a perspective transform on the image 
    if len(intersect_of_lines) == 4:
        pts1 = np.float32(intersect_of_lines)
        # starting with point with smallest x value
        pts1 = pts1[pts1[:,0].argsort()]
        # check if y value of first point is larger than second point
        # this is to make sure that the first point is the "bottom left" point
        if pts1[0][1] > pts1[1][1]:
            # if so, swap points
            pts1[[0, 1]] = pts1[[1, 0]]
        # check if y value of third point is larger than fourth point
        if pts1[2][1] > pts1[3][1]:
            # if so, swap points
            pts1[[2, 3]] = pts1[[3, 2]]
        pts2 = np.array([[0, 0], [height, 0], [0, width], [height, width]])

        M, status = cv.findHomography(pts1, pts2)
        im_out = cv.warpPerspective(frame, M, (height, width))
        im_out = cv.flip(im_out, 1)
    
    
    #######################################
    # putting the FPS count on the frame
    time = (cv.getTickCount() - e1)/ cv.getTickFrequency()
    e1 = cv.getTickCount()
    fps = 1/time
    average_fps = average_fps + (fps - average_fps)/100
    #######################################
    # Display the resulting frame
    # for phone portrait mode
    frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)
    edges = cv.rotate(edges, cv.ROTATE_90_CLOCKWISE)
    cv.putText(frame, str(np.round(fps,1)), (10, 50), font, 1, (255, 255, 0), 2, cv.LINE_AA)
    cv.putText(frame, str(np.round(average_fps,1)), (10, 100), font, 1, (125, 0, 255), 2, cv.LINE_AA)
    cv.imshow('edges',edges)
    cv.imshow('frame',frame)
    if len(intersect_of_lines) == 4:
        #im_out = cv.rotate(im_out, cv.ROTATE_90_CLOCKWISE)
        cv.imshow('Top down view', im_out)

    intersect_of_lines = []
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        # save the last frame
        cv.imwrite('.\images\last_frame.jpg', frame)
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()