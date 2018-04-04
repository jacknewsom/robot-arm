import cv2
import numpy as np

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

def find_centers(image, radius=5):
    '''Returns list of tuples of centers of skittles
    
    Makes use of thresholding and distance transforms
    '''
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
    
    locs = []
    x, y = centers.shape
    zeros = np.greater(centers, 0)
    for i in range(x):
        for j in range(y):
            if (not zeros[i ,j]):
                locs.append([j, i])
                # set surrounding area to white to avoid duplication
                centers[(i-radius):(i+radius), (j-radius):(j+radius)] = 255
    return locs

def draw_circles(image, radius=10):
    '''
    draw constant width circles on centers of skittles found by thresholding
    '''
    copy = np.copy(image)
    centers = find_centers(copy)
    for center in centers:
        copy = cv2.circle(copy, tuple(center), radius, (0, 0, 255), 1)

    return copy

def draw_contours(image, lower_bound=30, epsilon_scale=0.1):
    '''returns copy of image with contours drawn on'''
    copy = np.copy(image)
    threshold = binarize(np.copy(image), lower_bound)

    img, contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    centers, radii = [], []
    for contour in contours:
        epsilon = epsilon_scale * cv2.arcLength(contour, True)
        poly = cv2.approxPolyDP(contour, epsilon, True)
        center, radius = cv2.minEnclosingCircle(poly)
    
        if radius < 30:    
            center = (int(center[0]), int(center[1]))
            centers.append(center)
            radii.append(radius)
            
            cv2.putText(copy,'R' + str(radius)[:4], center, cv2.FONT_HERSHEY_SIMPLEX, 
                        1,(255,255,255),1,cv2.LINE_AA)


    drawing = cv2.drawContours(copy, contours, -1, (0, 255, 0), 1)
    return drawing, centers, radii