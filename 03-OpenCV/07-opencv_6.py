import cv2

cap = cv2.VideoCapture(1) #common source = 0

while (True):
    ret, frame = cap.read()
    cv2.line(frame, (320, 480), (320,0), (0,0,255),3)
    cv2.imshow("Original", frame)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
