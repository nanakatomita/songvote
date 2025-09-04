
from flask import Flask, jsonify
from flask_cors import CORS
import requests
from config import CLIENT_ID, CLIENT_SECRET, ARTIST_ID

app = Flask(__name__)
CORS(app)


def get_token():
    url = "https://accounts.spotify.com/api/token"
    res = requests.post(url, {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    })
    res.raise_for_status()
    return res.json()["access_token"]

@app.route("/songs")
def get_songs():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    albums_res = requests.get(
        f"https://api.spotify.com/v1/artists/{ARTIST_ID}/albums",
        headers=headers,
        params={"include_groups":"album,single","market":"JP","limit":50}
    ).json()

    songs = []
    for album in albums_res["items"]:
        album_id = album["id"]
        album_img = album["images"][0]["url"]
        tracks_res = requests.get(
            f"https://api.spotify.com/v1/albums/{album_id}/tracks",
            headers=headers,
            params={"market":"JP"}
        ).json()
        for t in tracks_res["items"]:
            songs.append({
                "name": t["name"],
                "img": album_img,
                "embed": f"https://open.spotify.com/embed/track/{t['id']}"
            })

    # 曲名で重複を削除
    seen = set()
    unique_songs = []
    for s in songs:
        if s["name"] not in seen:
            unique_songs.append(s)
            seen.add(s["name"])

    return jsonify(unique_songs)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
