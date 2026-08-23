import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BOT_TOKEN = os.environ.get("BOT_TOKEN")


@app.route("/api/photo", methods=["GET"])
def get_photo():
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({"error": "user_id required"}), 400

    if not BOT_TOKEN:
        return jsonify({"error": "BOT_TOKEN is not configured"}), 500

    try:
        resp = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/getUserProfilePhotos",
            params={"user_id": user_id, "limit": 1},
            timeout=10,
        )
        data = resp.json()

        if not data.get("ok"):
            return jsonify({"error": "Telegram API error"}), 500

        photos = data.get("result", {}).get("photos", [])

        if not photos:
            return jsonify({"photo_url": None})

        file_id = photos[0][-1]["file_id"]

        file_resp = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/getFile",
            params={"file_id": file_id},
            timeout=10,
        ).json()

        file_path = file_resp.get("result", {}).get("file_path")

        if not file_path:
            return jsonify({"photo_url": None})

        return jsonify({
            "photo_url": f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
