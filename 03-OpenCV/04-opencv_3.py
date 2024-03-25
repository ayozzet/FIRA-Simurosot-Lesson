import cv2

cap = cv2.VideoCapture(0) #common source = 0

while (True):
    ret, frame = cap.read()

    edge1 = cv2.Canny(frame, 100, 200)
    edge2 = cv2.Canny(frame, 10, 20)

    cv2.imshow("Original", frame)
    cv2.imshow("Canny 1", edge1)
    cv2.imshow("Canny 2", edge2)
    #print(edge)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
