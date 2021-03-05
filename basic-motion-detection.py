import cv2
import time
cap = cv2.VideoCapture(0) # Capturing the video via default camera
ret, frame1 = cap.read()
time.sleep(0.5) #delys 5seconds
ret, frame2 = cap.read()

while cap.isOpened() : # Loop to draw rectangles on large moving object
    diff = cv2.absdiff(frame1,frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0) # to make the image pixels black and white
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY) # is pixel intensity is greater than set threshold, value set is set to 255 else 0
    dilated = cv2.dilate(thresh, None, iterations=3) #Increases the size of the foreground/white region
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        
        if cv2.contourArea(contour) < 6000:
            continue
        cv2.rectangle(frame1, (x,y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame1, "Status: {}".format("Movement"), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    # cv2.drawContours(frame1, contours, -1, (0,255,0), 2) 
    cv2.imshow("Motion Detection Camera System", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()
    if cv2.waitKey(1) & 0xFF == ord('q'): #The program quits when the user presses "q"
        break

cv2.destroyAllWindows() # CLoses all the opened windows
cap.release() # Releases the video
