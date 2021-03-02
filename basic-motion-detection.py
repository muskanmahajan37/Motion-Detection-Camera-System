import cv2
cap = cv2.VideoCapture(0) # Capturing the video via default camera
ret, frame1 = cap.read()
ret, frame2 = cap.read()


while cap.isOpened() : # Loop to display every single frame from the captured video
    diff = cv2.absdiff(frame1,frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR.BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(frame1, contours, -1, (0,255,0), 2) 

    cv2.imshow("Motion Detection Camera System", frame1)
    if cv2.waitKey(1) & 0xFF == ord('q'): #The program quits when the user presses "q"
        break

cv2.destroyAllWindows() # CLoses all the opened windows
cap.release() # Releases the video
