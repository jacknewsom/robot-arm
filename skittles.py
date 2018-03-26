import cv2
import numpy as np
import math

def binarize(image, lower_bound=30):
    '''returns binary thresholded version of input image
    
    decreasing lower_bound will decrease sensitivity
    '''
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # we're only going to work w/ saturation channel of hsv image
    hue, saturation, value = cv2.split(hsv)

    # apply gaussian blur to smooth out edges
    gauss = cv2.GaussianBlur(saturation, (7, 7), 0)
    # apply thresholding to eliminate noise
    ret, threshold = cv2.threshold(gauss, lower_bound, 255, cv2.THRESH_BINARY)

    return threshold

def center_locations(image, radius=5):
    '''Returns list of tuples of centers of skittles '''
    locs = []
    x, y = image.shape
    zeros = np.greater(image, 0)
    for i in range(x):
        for j in range(y):
            if (not zeros[i ,j]):
                locs.append([j, i])
                # set surrounding area to white to avoid duplication
                image[(i-radius):(i+radius), (j-radius):(j+radius)] = 255
    return locs

def reduce_to_centers(image):
    '''given image of skittles, return image containing only black dots at skittle centers'''
    threshold = binarize(image, 50)

    # apply distance transform, will help us find skittle centers
    dist = cv2.distanceTransform(threshold, cv2.DIST_L2, 5)
    # normalize brightness values
    dist = cv2.normalize(dist, 0, 255, cv2.NORM_MINMAX)

    ret, threshold = cv2.threshold(dist, 1, 255, cv2.THRESH_TOZERO)

    kernel = np.ones((3,3), np.uint8)
    kernel = kernel / (kernel.shape[0] * kernel.shape[1])
    dilation = cv2.dilate(threshold, kernel, iterations=1)

    ret, threshold = cv2.threshold(dilation-dist, 0, 255, cv2.THRESH_BINARY)
    threshold = cv2.convertScaleAbs(threshold)

    # find background
    opening = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel, iterations=2)
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    inv_bg = cv2.bitwise_not(sure_bg)
    inv_bg = cv2.dilate(inv_bg, kernel, iterations=7)

    # add thresholded image to inverse background to isolate centers
    centers = threshold + inv_bg
    ret, centers = cv2.threshold(centers, 0, 255, cv2.THRESH_BINARY)
    return centers

def draw_circles(image, radius=10):
    '''returns copy of image with circles drawn on'''
    copy = np.copy(image)
    centers = reduce_to_centers(copy)
    locs = center_locations(centers)
    for loc in locs:
        copy = cv2.circle(copy, tuple(loc), radius, (0, 0, 255), 1)

    return copy

def draw_contours(image, lower_bound=30):
    '''returns copy of image with contours drawn on :) '''
    threshold = binarize(np.copy(image), lower_bound)
    copy = np.copy(image)

    img, contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    centers, radii = [], []
    for contour in contours:
        epsilon = 0.1 * cv2.arcLength(contour, True)
        poly = cv2.approxPolyDP(contour, epsilon, True)
        center, radius = cv2.minEnclosingCircle(poly)
        center = (int(center[0]), int(center[1]))
        centers.append(center)
        radii.append(radius)
        
        cv2.putText(copy,'R' + str(radius), center, cv2.FONT_HERSHEY_SIMPLEX, 
                    1,(255,255,255),1,cv2.LINE_AA)


    drawing = cv2.drawContours(copy, contours, -1, (0, 255, 0), 1)
    return drawing
