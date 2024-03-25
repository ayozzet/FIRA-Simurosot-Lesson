import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0) #common source = 0

while (True):
    ret, frame = cap.read()
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    low = np.array([30, 180, 180])
    high = np.array([35, 240, 255])
    mask1 = cv.inRange(hsv, low, high)
    yellow = cv.bitwise_and(frame, frame, mask = mask1)
    cv.imshow("Original", frame)
    cv.imshow("HSV", hsv)
    cv.imshow("Mask", mask1)
    cv.imshow("Detect", yellow)

    if cv.waitKey(1) & 0xFF ==ord('q'):
        break
cap.release()
cv.destroyAllWindows()
