from flask import Flask, render_template, Response
import cv2
import os
import time
import face_recognition
from picamera2 import Picamera2
import smtplib
from email.mime.text import MIMEText

app = Flask(_name_)

# Load known face encodings and names
known_face_encodings = []
known_face_names = []
known_faces_dir = "profiles"

for filename in os.listdir(known_faces_dir):
    if filename.endswith(".jpg"):
        name = os.path.splitext(filename)[0]
        image = face_recognition.load_image_file(os.path.join(known_faces_dir, filename))
        encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(encoding)
        known_face_names.append(name)

# Initialize face detector
face_detector = cv2.CascadeClassifier("/home/madhavv/Downloads/haarcascade_frontalface_default.xml")
cv2.startWindowThread()

# Initialize Picamera2
picam2_initialized = False
picam2 = None

def initialize_picam2():
    global picam2, picam2_initialized
    if not picam2_initialized:
        picam2 = Picamera2()
        picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (1280, 960)}))
        picam2.start()
        picam2_initialized = True

def send_email(subject, body):
    sender_email = "your_email@gmail.com"
    receiver_email = "your_email@gmail.com"
    email_password = "your_password"
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, email_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

def generate_frames():
    initialize_picam2()
    while True:
        im = picam2.capture_array()

        grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(grey, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            # Expand the detected face region
            x0, y0 = max(0, x - 20), max(0, y - 20)
            x1, y1 = min(im.shape[1], x + w + 20), min(im.shape[0], y + h + 20)

            # Calculate the inverted bounding box coordinates
            inverted_x0 = max(0, im.shape[1] - x1)
            inverted_y0 = y0
            inverted_x1 = min(im.shape[1], im.shape[1] - x0)
            inverted_y1 = y1

            # Extract face region
            face_region = im[y0:y1, x0:x1]

            # Convert face region to RGB (required for face_recognition library)
            face_rgb = cv2.cvtColor(face_region, cv2.COLOR_BGR2RGB)

            # Recognize faces
            face_encodings = face_recognition.face_encodings(face_rgb)
            face_names = []

            for face_encoding in face_encodings:
                # Check if the face matches any known face
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # If a match is found, use the known name
                if True in matches:
                    matched_index = matches.index(True)
                    name = known_face_names[matched_index]

                face_names.append(name)

            # Display the name of the recognized face with inverted bounding box
            for name, (x0, y0, x1, y1) in zip(face_names, faces):
                # Use the inverted bounding box coordinates
                cv2.rectangle(im, (inverted_x0, y0), (inverted_x1, y1), (0, 255, 0), 2)
                cv2.putText(im, name, (inverted_x0, y0 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # If the face is unknown, display an alert
                if name == "Unknown":
                    cv2.putText(im, "ALERT: Unknown Person Detected!", (inverted_x0, y0 - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    send_email("Security Alert", "ALERT: Unknown Person Detected!")

        ret, buffer = cv2.imencode('.jpg', im)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if _name_ == '_main_':
    app.run(host='0.0.0.0', debug=True)