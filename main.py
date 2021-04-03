from flask import Flask,render_template,request,redirect,session,Response
import mysql.connector
import os

import cv2
import playsound
import threading
lock = threading.Lock() #This will help us perform synchronization; ex:to stop other threads from sending more emails

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

app=Flask(__name__)
app.secret_key=os.urandom(24)

conn=mysql.connector.connect(host="localhost", user="root",password="",database="MDCS")
cursor=conn.cursor()

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
        print("Warning message has been sent to {}".format(recipientEmail))
        server.close()
    except Exception as e:
    	print(e)

# threading.Thread(target=send_mail_function).start()

def play_alarm_sound_function():
    	while True:
		playsound.playsound('Alarm Sound.mp3',True)

def gen():
    cap = cv2.VideoCapture(0) # Capturing the video via default camera
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    alarm_triggered = False
    email_sent = False

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
        # cv2.imshow("Motion Detection Camera System", frame1)
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame1 + b'\r\n\r\n')
        # yield(frame1)
        frame1 = frame2
        ret, frame2 = cap.read()
    cv2.destroyAllWindows() # CLoses all the opened windows
    cap.release() # Releases the video

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('index.html')
    else:
        return redirect('/')

@app.route('/login_validation', methods=['POST'])
def login_validation():
    username=request.form.get('username')
    password=request.form.get('password')
    cursor.execute("SELECT * FROM `users` WHERE `username` LIKE '{}' AND `password` LIKE '{}'".format(username,password))
    users=cursor.fetchall()

    if len(users)>0:
        session['user_id']=users[0][0]
        return render_template("index.html")
    else:
        warning="Username or password is incorrect, try again!"
        return render_template("login.html", warning=warning)

@app.route("/register_user", methods=['POST'])
def register_user():
    newUsername=request.form.get('newUsername')
    newEmail=request.form.get('newEmail')
    newPassword=request.form.get('newPassword')
    cursor.execute("INSERT INTO `users` (`username`, `email`, `password`) values ('{}', '{}', '{}')".format(newUsername, newEmail, newPassword))
    conn.commit()
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('user_id')
    return redirect('/')


if __name__=="__main__":
    app.run(debug=True)