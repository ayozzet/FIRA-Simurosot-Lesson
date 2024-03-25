import cv2

cap =  cv2.VideoCapture(2)

while (True):
    ret, frame = cap.read()
    frame = cv2.resize(frame, (480, 270))
    # print(frame.shape)
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imshow("Original", frame)
    cv2.imshow("Grayscale", grayscale)
    cv2.imshow("HSV", hsv)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()