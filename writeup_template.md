# **Finding Lane Lines on the Road** 

## Writeup

---

**Finding Lane Lines on the Road**

The goals / steps of this project are the following:
* Make a pipeline that finds lane lines on the road
* Reflect on your work in a written report


[//]: # (Image References)

[image1]: ./test_images/out_solidWhiteRight.png "Lanes Detected"

---

### Reflection

### 1. Describe your pipeline. As part of the description, explain how you modified the draw_lines() function.

My pipeline consisted of 5 steps. First, I converted the images to grayscale, then I detected the edges in the image using the canny algorithm. Third I blurred the lines using a gaussian distribution, then I croped a region of interest of the image. Finally I searched for lines in the hough space of the image.

In order to draw a single line on the left and right lanes, I modified the draw_lines() function by separating the the left from the right lines using a threshold for the found line points to be in. Then I filter lines that can not be side lines because they have a wrong orientation. After that I use the remaining lines to calculate the the average of them. Finally I extend this average line from the bottom of the image to the middle of the image to predict the line in that area.

If you'd like to include images to show how the pipeline works, here is how to include an image: 

![alt text][image1]


### 2. Identify potential shortcomings with your current pipeline


One potential shortcoming would be what would happen when more smaller lines are detected all over the picture due to shadows on the road, reflections in the wind shield or many other reasons. IF this happens, the average of the lanes I compute can become more inaccurate due to the outlier sensitivity of the mean. Also the prediction if the lanes is onyl correct for straight lane markings. For example this pipeline is not suited for corners or roundabounts.

Another shortcoming could be the fix region of interest where I search for lines. If the car drives on a hil the horizon can change quite drastically, reducing the accuracy of the lane detection.


### 3. Suggest possible improvements to your pipeline

A possible improvement would be to filter the prediction over the time achis. That is, to incorporate previous detections to smooth the current detection. This can be done with an IIR filter a low pass filter, or if we can define a model, with a Kalman filter.

Another potential improvement could be to track the horizon as well and adjust the region of interest according to it. Furthermore it could be beneficial to reshape the region of interest according to the steering angle.
