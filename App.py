from flask import Flask, render_template, request, session, flash

import mysql.connector
import base64, os


from flask import Flask, render_template, request, jsonify



app = Flask(__name__)
app.config['SECRET_KEY'] = 'aaa'



@app.route("/")
def homepage():
    return render_template('index.html')




@app.route('/AdminLogin')
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route('/UserLogin')
def UserLogin():
    return render_template('UserLogin.html')


@app.route('/NewUser')
def NewUser():
    return render_template('NewUser.html')


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    error = None
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['password'] == 'admin':

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1solarfault')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb ")
            data = cur.fetchall()
            flash("you are successfully Login")
            return render_template('AdminHome.html', data=data)

        else:
            flash("UserName or Password Incorrect!")
            return render_template('AdminLogin.html')


@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1solarfault')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb  ")
    data = cur.fetchall()
    return render_template('AdminHome.html', data=data)



@app.route("/Report")
def Report():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1solarfault')
    cur = conn.cursor()
    cur.execute("SELECT * FROM activitytb  ")
    data = cur.fetchall()
    return render_template('Report.html', data=data)
@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        username = request.form['uname']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1solarfault')
        cursor = conn.cursor()
        cursor.execute(
            "insert into regtb values('','" + name + "','" + mobile + "','" + email + "','" + address + "','" + username + "','" + password + "')")
        conn.commit()
        conn.close()
        flash("Record Saved!")

    return render_template('NewUser.html')


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['sname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1solarfault')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' and password='" + password + "'")
        data = cursor.fetchone()
        if data is None:
            flash('Username or Password is wrong')
            return render_template('UserLogin.html', data=data)

        else:

            session['mob'] =data[2]
            session['email'] = data[3]

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1solarfault')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where username='" + username + "' and password='" + password + "'")
            data = cur.fetchall()
            flash("you are successfully logged in")
            return render_template('UserHome.html', data=data)


@app.route('/UserHome')
def UserHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1solarfault')
    cur = conn.cursor()
    cur.execute("SELECT username FROM regtb  where username='" + session['sname'] + "' ")
    data = cur.fetchall()
    return render_template('DoctorHome.html', data=data)


@app.route('/Predict')
def Predict():
    return render_template('Predict.html')


@app.route("/imupload", methods=['GET', 'POST'])
def imupload():
    if request.method == 'POST':
        import cv2
        file = request.files['file']
        file.save('static/Out/Test.jpg')
        org = 'static/Out/Test.jpg'

        from ultralytics import YOLO
        import cv2

        # image = cv2.imread(import_file_path)
        image = cv2.imread(org)
        model = YOLO('runs/detect/solar/weights/best.pt')

        class_labels = ['faulty', 'no faulty']

        # Perform object detection
        results = model(image, conf=0.6)

        confidences = results[0].boxes.conf  # Confidence scores
        class_indices = results[0].boxes.cls  # Class indices

        if len(confidences) > 0:
            max_confidence_index = confidences.argmax().item()  # Get index of highest confidence
            predicted_class_index = int(class_indices[max_confidence_index].item())  # Get correct class index

            # Ensure index is within bounds
            if 0 <= predicted_class_index < len(class_labels):
                predicted_class = class_labels[predicted_class_index]  # Map index to label
            else:
                predicted_class = "Unknown Class"

            confidence_score = confidences[max_confidence_index].item()  # Get highest confidence score

            print(f"Predicted Class: {predicted_class}")
            print(f"Confidence Score: {confidence_score:.4f}")  # Display with 4 decimal places
        else:
            predicted_class = "No Detections"
            confidence_score = 0.0
            print("No objects detected.")



        # Optionally, visualize the results
        annotated_frame = results[0].plot()
        outi = "static/Out/out.jpg"
        cv2.imwrite("static/Out/out.jpg", annotated_frame)

        # Display the annotated frame
        cv2.imshow("YOLOv8 Inference", annotated_frame)
        # cv2.waitKey(0)
        cv2.destroyAllWindows()

        return render_template('Predict.html', res=predicted_class, outi=outi)



@app.route("/Camera")
def Camera():
    import cv2
    from ultralytics import YOLO

    # Load the YOLOv8 model
    model = YOLO('runs/detect/solar/weights/best.pt')
    # Open the video file
    # video_path = "path/to/your/video/file.mp4"
    cap = cv2.VideoCapture(0)
    dd1 = 0

    # Loop through the video frames
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()

        if success:
            # Run YOLOv8 inference on the frame
            results = model(frame, conf=0.6)
            for result in results:
                if result.boxes:
                    box = result.boxes[0]
                    class_id = int(box.cls)
                    object_name = model.names[class_id]
                    print(object_name)

                    if object_name == 'faulty':
                        dd1 += 1
                        print(dd1)

                    if dd1 == 50:
                        dd1 = 0
                        import winsound

                        filename = 'alert.wav'
                        winsound.PlaySound(filename, winsound.SND_FILENAME)

                        annotated_frame = results[0].plot()

                        cv2.imwrite("alert.jpg", annotated_frame)
                        import random
                        loginkey = random.randint(1111, 9999)
                        imgg = "static/upload/" + str(loginkey) + ".jpg"
                        cv2.imwrite(imgg, annotated_frame)
                        import datetime
                        date = datetime.datetime.now().strftime('%Y-%m-%d')

                        time = datetime.datetime.now().strftime('%H:%M:%S')

                        conn = mysql.connector.connect(user='root', password='', host='localhost',
                                                       database='1solarfault')
                        cursor = conn.cursor()
                        cursor.execute(
                            "INSERT INTO activitytb VALUES ('','"+ session['sname'] +"','" + date + "','" + time + "','" + object_name + "','" + str(
                                imgg) + "')")
                        conn.commit()
                        conn.close()


                        sendmail( session['email'])
                        sendmsg(session['mob'], "Prediction Name:" + object_name)

            # Visualize the results on the frame
            annotated_frame = results[0].plot()

            # Display the annotated frame
            cv2.imshow("YOLOv8 Inference", annotated_frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    # Release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()


def sendmsg(targetno, message):
    import requests
    requests.post(
        "http://sms.creativepoint.in/api/push.json?apikey=6555c521622c1&route=transsms&sender=FSSMSS&mobileno=" + targetno + "&text=Dear customer your msg is " + message + "  Sent By FSMSG FSSMSS")


def sendmail(mail):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    fromaddr = "projectmailm@gmail.com"
    toaddr = mail

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Alert"

    # string to store the body of the mail
    body = " Solar Panel Fault Detection"

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = "alert.jpg"
    attachment = open("alert.jpg", "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "qmgn xecl bkqv musr")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
