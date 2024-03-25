import cv2

cap = cv2.VideoCapture(0) #common source = 0

while (True):
    ret, frame = cap.read()

    blur1 = cv2.GaussianBlur(frame, (15,15), 0)
    blur2 = cv2.GaussianBlur(frame, (101,101), 0)

    cv2.imshow("Original", frame)
    cv2.imshow("Blur 1", blur1)
    cv2.imshow("Blur 2", blur2)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
