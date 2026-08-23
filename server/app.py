import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='../static')
CORS(app)  # разрешаем запросы с любого домена

BOT_TOKEN = os.environ.get("BOT_TOKEN")  # токен твоего бота

# Эндпоинт для получения аватарки
@app.route('/api/photo', methods=['GET'])
def get_photo():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id required"}), 400

    # Запрос к Bot API
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUserProfilePhotos"
    params = {"user_id": user_id, "limit": 1}
    
    try:
        resp = requests.get(url, params=params)
        data = resp.json()
        if not data.get("ok"):
            return jsonify({"error": "Telegram API error"}), 500

        photos = data.get("result", {}).get("photos", [])
        if not photos:
            return jsonify({"photo_url": None})  # нет фото

        # берём самое большое фото (последний элемент в массиве)
        file_id = photos[0][-1]["file_id"]
        # получаем путь к файлу
        file_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
        file_resp = requests.get(file_url).json()
        file_path = file_resp.get("result", {}).get("file_path")
        if not file_path:
            return jsonify({"photo_url": None})

        photo_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
        return jsonify({"photo_url": photo_url})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Отдаём index.html (опционально)
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
