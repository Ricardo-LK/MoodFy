from flask import Flask, render_template, Response
from deepface import DeepFace
import cv2
import sys

app = Flask(__name__)

camera = cv2.VideoCapture(0)


def getEmotion(frame):
    try:
        print("Entrei")
        analyze = DeepFace.analyze(frame, actions=["emotion"])  # Using the captured frame to get all the recognized emotions
        emotion = analyze[0]["dominant_emotion"]  # Getting the primary emotion
        print(emotion)
        return emotion
    except:
        print("No face")

def get_frames():
    while True:
        _, frame = camera.read()

        ret, buffer = cv2.imencode('.jpg',frame)
        frame = buffer.tobytes()

        key =  cv2.waitKey(33)
        # Key that will stop the loop and stop the video (ESC)
        if key == 27:   
            break
        elif key == 13:  # Key that will take the current frame (ENTER)
            sys.stdout("a")
            emotion = getEmotion(frame)
            # If current frame contains face returns emotion and exit loop else feedback and keep running 
            if emotion is not None:
                print(emotion)
                camera.release()
        
        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')

def index():
    return render_template('moodFy.html')

@app.route('/video')

def video():
    return Response(get_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)