# Assignment 2


## Part I - Line detector

![image 1](./images/first_Canny.jpg)

Example frame from using the Canny edge detector, with lower threshold 100 and upper threshold 200.

![image 2](./images/second_Canny.jpg)

Again with, but with lower threshold 75 and upper threshold 125.

### RANSAC

After playing with the parameters I got the RANSAC algorithm to work. I halved the size of the image so the performance would be better. The number of samples was set at 20 and the distance threshold was at 5 pixels. Obviously it got better with more samples, but then the performance was really slow. With these parameters the fps was around 15 to 18. When holding the papar in front of the camera the line sometimes jumped from the edges on the closet and to the edges on the door. The line was displayed on the live image and the line follwed a sheet of paper very well. The processing time as can be seen from the fps counter was about 60 ms per frame.

![image 3](./images/1.jpg)

![image 4](./images/2.jpg)

## Part II - Rectification

![image 5](./images/rectification1.jpg)

In the picture above there are 4 lines detected and 4 points of intersection. I have been trying to do a perspective transformation on the enclosed rectangular area, but it has not been working very well. For some reason the lines glitch in and out of the frame, so often it shows only 2 lines detected even though there are clearly 4 lines.