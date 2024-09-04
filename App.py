import base64
import os
import webbrowser
import cv2
from flask import Flask, render_template, Response, request
from deepface import DeepFace
from dotenv import load_dotenv
from requests import post, get

load_dotenv()

app = Flask(__name__)

camera = cv2.VideoCapture(0)
tracks_limit = 5

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

platform = "spotify"

def get_spotify_token():
    auth_string = f"{client_id}:{client_secret}"
    auth_base64 = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}

    result = post(url, headers=headers, data=data)
    result.raise_for_status()
    json_result = result.json()
    return json_result["access_token"]

def get_spotify_auth_header(token):
    return {"Authorization": f"Bearer {token}"}

def get_spotify_genres(emotion):
    genres = {
        "happy": "pop, anime, disco, k-pop, reggaeton",
        "neutral": "chill, ambient, alternative, classical, jazz",
        "angry": "metal, death-metal, hardcore-punk, punk, hard-rock",
        "disgust": "industrial, black-metal, grindcore, punk-rock",
        "fear": "goth, industrial, black-metal, horrorcore",
        "sad": "blues, emo, folk, grunge, sad",
        "surprise": "progressive-house, alternative, psych-rock, alt-rock, j-pop"
    }
    return genres.get(emotion, "")

def search_spotify_tracks_by_genres(token, genres):
    url = "https://api.spotify.com/v1/recommendations"
    headers = get_spotify_auth_header(token)
    query = f"?seed_genres={genres}&limit={tracks_limit}"

    query_url = url + query
    result = get(query_url, headers=headers)
    result.raise_for_status()
    json_result = result.json()
    return json_result.get("tracks", [])


def search_youtube_tracks_by_genre(genres):
    return webbrowser.open(f"https://www.youtube.com/results?search_query={genres}+song")    

def getEmotion(frame):
    try:
        analyze = DeepFace.analyze(frame, actions=["emotion"])
        emotion = analyze[0]["dominant_emotion"]
        print(emotion)
        return emotion
    except:
        print("No face detected")
        return None

def get_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('moodFy.html')

@app.route('/video')
def video():
    return Response(get_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/select_platform', methods = ['GET', 'POST'])
def select_platform():
    global platform
    if request.method == "POST":
        try:
            platform = request.form.get("variable")
        except:
            print("Wrong")

    return render_template('moodFy.html', platform = platform)

@app.route('/capture_emotion', methods=['POST'])
def capture_emotion():
    success, frame = camera.read()
    if success:
        emotion = getEmotion(frame)
        print(emotion)
        if emotion:
            if platform == "spotify":
                token = get_spotify_token()
                genres = get_spotify_genres(emotion)
                if genres:
                    tracks = search_spotify_tracks_by_genres(token, genres)
                    return render_template('moodFy.html', emotion = emotion, tracks = tracks, platform = platform)
            elif platform == "youtube":
                print("Youtube")
                search_youtube_tracks_by_genre(emotion)
                return render_template('moodFy.html', emotion = emotion, tracks = [], platform = platform)


    return render_template('moodFy.html', emotion="No face detected or no tracks found", tracks=[], platform = platform)

if __name__ == "__main__":
    app.run(debug=True)