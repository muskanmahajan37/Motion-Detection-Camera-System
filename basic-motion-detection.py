import cv2
import numpy as numpy
cap = cv2.videoCapture(0)

while cap.isOpened() :
    ret, frame = cap.read()

    cv2.imshow("inter", frame)

    if cv2.waitKey(40) == 27:
        break

cv2.destroyAllWindows()
cap.release()