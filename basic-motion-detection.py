import cv2
cap = cv2.VideoCapture(0) # Capturing the video via default camera

while cap.isOpened() : # Loop to display every single frame from the captured video
    ret, frame = cap.read()
    cv2.imshow("Motion Detection Camera System", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): #The program quits when the user presses "q"
        break

cv2.destroyAllWindows() # CLoses all the opened windows
cap.release() # Releases the video
