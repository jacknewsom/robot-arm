import cv2
import numpy as np
import matplotlib.pyplot as plt


img = cv2.imread('skittles.png', -1)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

hue, saturation, value = cv2.split(hsv)

gauss = cv2.GaussianBlur(saturation, (7, 7), 0)
ret, thresh = cv2.threshold(gauss, 30, 255, cv2.THRESH_BINARY)

dist = cv2.distanceTransform(thresh, cv2.DIST_L2, 5)
dist = cv2.normalize(dist, 0, 255, cv2.NORM_MINMAX)

ret, threshold = cv2.threshold(dist, 1, 255, cv2.THRESH_TOZERO)

kernel = np.ones((3,3), np.uint8)
dilation = cv2.dilate(threshold, kernel, iterations=1)

depeaked = dilation - dist

ret, threshold = cv2.threshold(depeaked, 0, 255, cv2.THRESH_BINARY)
threshold = cv2.convertScaleAbs(threshold)

# find background
opening = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel, iterations=2)
sure_bg = cv2.dilate(opening, kernel, iterations=1)
inv_bg = cv2.bitwise_not(sure_bg)


'''
TODO
- figure out contour
- need to isolate peaks within image (aka skittle centers!)
- then thats it, i think
'''



cv2.imshow("image", threshold)
cv2.waitKey(0)
cv2.destroyAllWindows()