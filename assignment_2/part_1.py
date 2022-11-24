import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import warnings

# turn off warnings
warnings.filterwarnings("ignore")
# capture video from camera
cap = cv.VideoCapture(1)

font = cv.FONT_HERSHEY_SIMPLEX
average_fps = 0
e1 = cv.getTickCount()

def RANSAC(points, distance_threshold, samples):
    best_inliers = 0
    best_model = None
    for i in range(samples):
        # randomly select 2 points
        random_points = np.random.randint(0,points.shape[0], 2)
        random_points = points[random_points]
        # calculate line model
        model = np.polyfit(random_points[:, 0], random_points[:, 1], 1)
        # how many points lie within the distance threshold
        inliers = 0
        for point in points:
            distance = abs(model[0] * point[0] + model[1] - point[1]) / np.sqrt(model[0] ** 2 + 1)
            if distance < distance_threshold:
                inliers += 1
        # if the number of inliers is greater than the current best, update the best
        if inliers > best_inliers:
            best_inliers = inliers
            best_model = model
    return best_model

dist_thresh = 1 # pixel distance threshold
N_samples = 70  # number of random samples from edge points

while(True):
    # Capture frame-by-frame
    try:
        ret, frame = cap.read()
        # reduce size of input image
        frame = cv.resize(frame, (0,0), fx=0.4, fy=0.4)

        # convert to grayscale
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # reduce noise with median filter
        gray = cv.medianBlur(gray, 5)
        # Canny edge detection
        edges = cv.Canny(gray, 150, 200)

        # store coordinates of edges in array
        edge_coordinates = np.where(edges == 255)
        # store as x,y coordinates
        edge_coordinates = np.array([edge_coordinates[1], edge_coordinates[0]]).T


        # RANSAC
        model = RANSAC(edge_coordinates, dist_thresh, N_samples)
        # draw line on image
        x = np.array([0, frame.shape[1]])
        y = model[0] * x + model[1]
        cv.line(frame, (int(x[0]), int(y[0])), (int(x[1]), int(y[1])), (0, 255, 0), 2)

        # putting the FPS count on the frame
        time = (cv.getTickCount() - e1)/ cv.getTickFrequency()
        e1 = cv.getTickCount()
        fps = 1/time
        average_fps = average_fps + (fps - average_fps)/100
        cv.putText(frame, str(np.round(fps,1)), (10, 50), font, 1, (255, 255, 0), 2, cv.LINE_AA)
        cv.putText(frame, str(np.round(average_fps,1)), (10, 100), font, 1, (125, 0, 255), 2, cv.LINE_AA)

        # Display the resulting frame
        cv.imshow('frame',frame)
        cv.imshow('edges',edges)
        if cv.waitKey(1) & 0xFF == ord('q'):
            # save the last frame
            cv.imwrite('.\images\last_frame.jpg', frame)
            break
    except:
        pass

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()


""" # make array of random x, y coordinates
points = np.random.randint(0, 100, (15, 2))

#print(points)
dist_thresh = 10
r = RANSAC(points, dist_thresh, 10)
#print(r)

# plot points 
plt.scatter(points[:, 0], points[:, 1])
# plot line
plt.plot(points[:, 0], np.polyval(r[0], points[:, 0]), 'r')
# plot distance threshold
plt.plot(points[:, 0], np.polyval(r[0], points[:, 0]) + dist_thresh, 'g')
plt.plot(points[:, 0], np.polyval(r[0], points[:, 0]) - dist_thresh, 'g')

# print how many inliers
print(len(r[1]))
plt.show() """