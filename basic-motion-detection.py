import cv2
import playsound
import threading
lock = threading.Lock() #This will help us perform synchronization; ex:to stop other threads from sending more emails

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

cap = cv2.VideoCapture(0) # Capturing the video via default camera
ret, frame1 = cap.read()
ret, frame2 = cap.read()
alarm_triggered = False
email_sent = False

def send_mail_function():
    senderEmail = "robeehacks@gmail.com"
    senderPassword = "1pa2345w"
    recipientEmail = "peacecyebukayire@gmail.com"
    recipientEmail = recipientEmail.lower()
    Email_subject = "Intruder Has Been Detected!"
    Email_body = "Warning! An intruder has been reported in ABC Room"
    message = 'Subject: {}\n\n{}'.format(Email_subject, Email_body)
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(senderEmail, senderPassword)
        server.sendmail(senderEmail, recipientEmail, message)
        print("sent to {}".format(recipientEmail))
        server.close()
    except Exception as e:
    	print(e)

# threading.Thread(target=send_mail_function).start()

def play_alarm_sound_function():
    	while True:
		playsound.playsound('Alarm Sound.mp3',True)

while cap.isOpened() : # Loop to draw rectangles on large moving object
    diff = cv2.absdiff(frame1,frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0) # to make the image pixels black and white
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY) # is pixel intensity is greater than set threshold, value set is set to 255 else 0
    dilated = cv2.dilate(thresh, None, iterations=3) #Increases the size of the foreground/white region
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        
        if cv2.contourArea(contour) > 4000:
            cv2.rectangle(frame1, (x,y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame1, "Status: {}".format("Intruder"), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            with lock:
                if not email_sent:
                    threading.Thread(target=send_mail_function).start()
                    email_sent = True
                # if not alarm_triggered:
                #     threading.Thread(target = play_alarm_sound_function).start()
                #     alarm_triggered = True

    # cv2.drawContours(frame1, contours, -1, (0,255,0), 2) 
    cv2.imshow("Motion Detection Camera System", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()
    if cv2.waitKey(1) & 0xFF == ord('q'): #The program quits when the user presses "q"
        break

cv2.destroyAllWindows() # CLoses all the opened windows
cap.release() # Releases the video
