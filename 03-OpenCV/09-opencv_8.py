import numpy as np
import cv2
import math

#pixel columns n rows
lineCY = 220
lineCX = 320

def show_center():
    index = np.asarray(get[0])  #convert values at 219th rows in array
    #print (index)
    if index.size > 0 :         #handling value if existed, bypass if NULL
        index_left = index[0]   #define first index from left (first index)
        index_right = index[-1] #define first index from right (last index)
        #global center
        center = int(((index_right-index_left)/2)+index_left)   #define marker point at 219th rows
        #print(index_left, "--(",center,")--", index_right)
        cv2.line(frame, (center,lineCY),(center,lineCY-20),(0,0,255),2) #draw line from center line to marker point
        return center
    #else:
        #print ("NO") #stop the ESC and try to reverse a few step back
    #return center
def drawText():
    if center is not None:      #handling value if existed, bypass if NULL
        #global val_from_line
        val_from_line = (center -lineCX) #calculate distance from center to marker point in pixels
        #print (center)
        #print (val_from_line)
        cv2.putText(frame, str(val_from_line), (center-20,lineCY-30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255), 2, cv2.LINE_AA) #display value of distance in pixels
        #cv2.putText(frame, (int(val_from_line), (20,20), cv2.FONT_HERSHEY_SIMPLEX, 12, (255), 1, cv2.LINE_AA)
        return val_from_line
    else:
        cv2.putText(frame, "UNDETECTED", (lineCX-105,lineCY-100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA) #display IF no data capture at 219th rows

def degree_angle():
    if (center is not None) and (lineCY is not None):       #handling value if existed, bypass if NULL
        cv2.line(frame, (320,480),(center, lineCY), (0,255,0),2)  #draw line from center bottom to marker point
        cv2.line(frame, (320, lineCY), (center, lineCY), (125, 125, 125), 2) #draw line from center line to marker point
        adjacent = lineCY           #define value for adjacent
        opposite = center -lineCX   #define value for opposite
        #print (opposite)
        theta = int (math.degrees(math.atan(opposite/adjacent))) #find radian value between adjacent and opposite sides and then convert it into degree
        thetaText = str(theta) + " degree"  #convert degree value into strings and the combine with another strings
        cv2.putText(frame, thetaText, (center-20,lineCY-50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (175,100), 2, cv2.LINE_AA)  #display value of degree on input frame
        #print (int (theta))
        return theta

def servo():
    if degree is not None:      #handling value if existed, bypass if NULL
        #print (degree)
        if degree < 0:      #decide for negative value captured
            #steer left
            #print ("")
            valServo = int((-6*degree/5)+90)    #calibration for servo output
            if valServo >= 150:     #setting servo limit for value more than 150 degree
                outServo = 150
            else:
                outServo = valServo
            #print (valServo)
        elif degree > 0:        #decide for positive value captured
            #steer right
            #print ("")
            valServo = int((-4*degree/5)+90)    #calibration for servo output
            if valServo <= 50:      #setting servo limit for value less than 50 degree
                outServo = 50
            else:
                outServo = valServo
            #print (valServo)
        else:                   #decide for zero value captured
            #straight
            #print ("Straight")
            valServo = int(degree)  #equalize degree with servo output
            #print (valServo)
            outServo = valServo
        return outServo
    else:       #handling NULL value if existed
        #reverse
        print ("REVERSE")

cap = cv2.VideoCapture(0)   #common source = 0, secondary source = 1
#print (cap)
while(True):    #forever loop
    ret, frame = cap.read()     #define captured image/video
    #print(frame.shape)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)    #convert BGR to HSV
    blur = cv2.GaussianBlur(hsv,(15,15),0)          #blur the input

    low_yellow = np.array([20, 110, 180 ])          #min range of colour
    high_yellow = np.array ([50, 200, 230])         #max range of colour
    yellow_mask = cv2.inRange(blur, low_yellow, high_yellow)    #masking between two range of colour
    yellow = cv2.bitwise_and(frame, frame, mask=yellow_mask)    #masking mask with input frame

    edge = cv2.Canny(yellow, 100, 200)      #edge detection using Canny

    pix = np.asarray(edge)      #convert Canny image into array
    #print(edge.shape)
    get = np.where(pix[lineCY-1] == 255) # find 255 value at 219th rows
    print(get[0])                       #display values at 219th rows in one row array
    center = show_center()
    val_from_center = drawText()
    #val_from_line = int(lineC - center)
    #print (val_from_center)
    #print (center)
    degree = degree_angle()
    #print (degree)
    Servo = servo()
    print(Servo)
    cv2.line(frame, (320,0),(320,480),(0,255,0),2) #reference center line (vertical)

    cv2.imshow("Original", frame)
    #cv2.imshow("HSV", hsv)
    #cv2.imshow("Mask", yellow_mask)
    #cv2.imshow("Detected", yellow)
    cv2.imshow("Canny", edge)
    if cv2.waitKey(1) & 0xFF == ord('q'):   #press 'q' to stop running script
        break

cap.release()   #turn off video capturing
cv2.destroyAllWindows() #close all windows displayed
