import cv2
import numpy as np

# open sample image
img = cv2.imread('skittles.png', -1)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# we're only going to work w/ saturation channel of hsv image
hue, saturation, value = cv2.split(hsv)

# apply gaussian blur to smooth out edges
gauss = cv2.GaussianBlur(saturation, (7, 7), 0)
# apply thresholding to eliminate noise
ret, threshold = cv2.threshold(gauss, 30, 255, cv2.THRESH_BINARY)

# apply distance transform, will help us find skittle centers
dist = cv2.distanceTransform(threshold, cv2.DIST_L2, 5)
# normalize brightness values
dist = cv2.normalize(dist, 0, 255, cv2.NORM_MINMAX)

ret, threshold = cv2.threshold(dist, 1, 255, cv2.THRESH_TOZERO)

kernel = np.ones((3,3), np.uint8)
dilation = cv2.dilate(threshold, kernel, iterations=1)

ret, threshold = cv2.threshold(dilation-dist, 0, 255, cv2.THRESH_BINARY)
threshold = cv2.convertScaleAbs(threshold)

# find background
opening = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel, iterations=2)
sure_bg = cv2.dilate(opening, kernel, iterations=3)
inv_bg = cv2.bitwise_not(sure_bg)
inv_bg = cv2.dilate(inv_bg, kernel, iterations=7)

# add thresholded image to inverse background to isolate centers
threshold = threshold + inv_bg

cv2.imshow("img", threshold)
cv2.waitKey(0)
cv2.destroyAllWindows()