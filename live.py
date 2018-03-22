import cv2
import numpy as np
from isolate_centers import find_skittles

video = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
ticker = 0

while(video.isOpened()):
    ticker += 1
    ret, frame = video.read()

    if (ticker % 10 == 0):   
        drawing = find_skittles(frame)
        cv2.imshow('img', drawing)
        out.write(drawing)
        ticker = 0

    cv2.imshow('live', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
out.release()
cv2.destroyAllWindows()