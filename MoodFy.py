import cv2
from deepface import DeepFace

# Getting a haarcascade xml file
face_cascade_name = cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml'
face_cascade = cv2.CascadeClassifier()

# Handling fallback event
if not face_cascade.load(cv2.samples.findFile(face_cascade_name)):
    print("Error loading xml file")

# Requisting the input from the webcam or camera
video = cv2.VideoCapture(0)  

def getEmotion(frame):
    try:
        print("Entrei")
        analyze = DeepFace.analyze(frame, actions=["emotion"])  # Using the captured frame to get all the recognized emotions
        emotion = analyze[0]["dominant_emotion"]  # Getting the primary emotion
        print(emotion)
        return emotion
    except:
        print("No face")

def Mood():
    while True:
        _,frame = video.read()

        cv2.imshow('video', frame)

        key =  cv2.waitKey(33)
        # Key that will stop the loop and stop the video (ESC)
        if key == 27:   
            break
        elif key == 13:  # Key that will take the current frame (ENTER)
            emotion = getEmotion(frame)
            # If current frame contains face returns emotion and exit loop else feedback and keep running 
            if emotion != None:
                video.release()
                return emotion
