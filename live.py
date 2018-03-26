import cv2
import numpy as np
from skittles import *

video = cv2.VideoCapture(0)

while(cv2.waitKey(1) & 0xFF != ord('q')):
    ret, frame = video.read()


    param = 30
    drawing = draw_circles(frame)
    contours = draw_contours(frame, param)
    binarized = binarize(np.copy(frame), param)

    cv2.imshow('bin', binarized)
    cv2.imshow('circles', drawing)
    cv2.imshow('contours', contours)
    # cv2.imshow('live', frame)

video.release()
cv2.destroyAllWindows()