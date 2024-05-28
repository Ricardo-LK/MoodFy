import base64
from dotenv import load_dotenv
import json
import os
from requests import post, get

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
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

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

tracks_limit = 5
def search_tracks_by_genre(token, genre):
    url = "https://api.spotify.com/v1/recommendations"
    header = get_auth_header(token)
    query = f"?seed_genres={genre}&limit={tracks_limit}"

    query_url = url + query
    result = get(query_url, headers = header)
    json_result = json.loads(result.content)
    if len(json_result) < 1:
        print("Nenhuma musica com este genero")
        return None
    
    #print(json_result["tracks"])
    return json_result["tracks"]

token = get_token()
tracks = search_tracks_by_genre(token, "rock-n-roll")

for i, song in enumerate(tracks):
    print(f"{i + 1}: {song["name"]}")