import cv2
import numpy as np
from skittles import *

video = cv2.VideoCapture(0)
param = 30

while(cv2.waitKey(1) & 0xFF != ord('q')):
    ret, frame = video.read()

    drawing = draw_circles(frame)
    contours, centers, radii = draw_contours(frame, param)
    binned = binarize(frame, param)
    cv2.imshow('binned', binned)
    cv2.imshow('contours', contours)

video.release()
cv2.destroyAllWindows()