import base64
import json
import MoodFy
import os
from dotenv import load_dotenv
from requests import post, get


load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_spotify_token():
    auth_string = client_id + ":" + client_secret
    auth_base64 = str(base64.b64encode(auth_string.encode("utf-8")), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}

    result = post(url, headers = headers, data = data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]

    return token

def get_spotify_auth_header(token):
    return {"Authorization": "Bearer " + token}


def get_spotify_genres():
    genres = ""
    mood = MoodFy.Mood()

    match mood:
        case "happy":
            genres = "pop, anime, disco, k-pop, reggaeton"
            
        case "neutral":
            genres = "chill, ambient, alternative, classical, jazz"

        case 'angry':
            genres = "metal, death-metal, hardcore-punk, punk, hard-rock"

        case 'disgust':
            genres = "industrial, black-metal, grindcore, punk-rock"

        case 'fear':
            genres = "goth, industrial, black-metal, horrorcore"

        case 'sad':
            genres = "blues, emo, folk, grunge, sad"

        case 'surprise':
            genres = "progressive-house, alternative, psych-rock, alt-rock, j-pop"

    return genres

tracks_limit = 5
def search_spotify_tracks_by_genres(token, genres):
    url = "https://api.spotify.com/v1/recommendations"
    header = get_spotify_auth_header(token)
    query = f"?seed_genres={genres}&limit={tracks_limit}"

    query_url = url + query
    result = get(query_url, headers = header)
    json_result = json.loads(result.content)
    if len(json_result) < 1:
        print("Nenhuma musica com este genero")
        return None
    
    #print(json_result["tracks"])
    return json_result["tracks"]

token = get_spotify_token()
genres = get_spotify_genres()
tracks = search_spotify_tracks_by_genres(token, genres)

for i, song in enumerate(tracks):
    print(f"{i + 1}: {song["name"]}")