import cv2
import numpy as np
from skittles import find_skittles

video = cv2.VideoCapture(0)

while(cv2.waitKey(1) & 0xFF != ord('q')):
    ret, frame = video.read()

    drawing = find_skittles(frame)
    cv2.imshow('skittles', drawing)
    cv2.imshow('live', frame)

video.release()
cv2.destroyAllWindows()