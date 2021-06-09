from flask import Flask,render_template,request,redirect,session,Response
import mysql.connector
import os
from motionDetection import MotionDetection

app=Flask(__name__)
app.secret_key=os.urandom(24)

conn = mysql.connector.connect(host="localhost", user="root",password="",database="MDCS")
cursor=conn.cursor()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(MotionDetection()),
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
        # return render_template("session.py")
        # print("User Logged In Successfully")
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