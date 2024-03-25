import cv2

cap = cv2.VideoCapture(1) #common source = 0

while (True):
    ret, frame = cap.read()
    cv2.putText(frame, "AKHYAR", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2, cv2.LINE_AA )
    cv2.imshow("Original", frame)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
