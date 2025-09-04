from flask import Flask, jsonify
from flask_cors import CORS
import requests
import time
from config import CLIENT_ID, CLIENT_SECRET

app = Flask(__name__)
CORS(app)

cache = {"data": None, "timestamp": 0}
CACHE_TTL = 60 * 5  

def get_token():
    url = "https://accounts.spotify.com/api/token"
    res = requests.post(url, {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    })
    return res.json()["access_token"]

@app.route("/playlist/<playlist_id>")
def get_playlist_songs(playlist_id):
    global cache

    if cache["data"] and (time.time() - cache["timestamp"] < CACHE_TTL):
        return jsonify(cache["data"])

    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    res = requests.get(
        f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
        headers=headers,
        params={"market":"JP","limit":99}
    )

    
    if res.status_code == 429:
        wait = int(res.headers.get("Retry-After", 1))
        time.sleep(wait)
        res = requests.get(
            f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
            headers=headers,
            params={"market":"JP","limit":50}
        )

    songs = []
    for item in res.json().get("items", []):
        track = item.get("track")
        if not track: 
            continue
        songs.append({
            "name": track["name"],
            "img": track["album"]["images"][0]["url"],
            "embed": f"https://open.spotify.com/embed/track/{track['id']}"
        })

    cache["data"] = songs
    cache["timestamp"] = time.time()

    return jsonify(songs)

if __name__ == "__main__":
    app.run(debug=True)
