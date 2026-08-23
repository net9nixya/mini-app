from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# ПРАВИЛЬНОЕ ИМЯ БАЗЫ (как у тебя в файлах)
DB_PATH = os.environ.get("DB_PATH", "standleo_lite_bot.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/profile', methods=['GET'])
def get_profile():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id required"}), 400

    conn = get_db()
    user = conn.execute(
        "SELECT nickname, elo, gold, wins, losses, vips FROM users WHERE telegram_id = ?",
        (user_id,)
    ).fetchone()
    conn.close()

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "success": True,
        "nickname": user["nickname"],
        "elo": user["elo"],
        "gold": user["gold"],
        "wins": user["wins"],
        "losses": user["losses"],
        "vips": user["vips"]
    })

@app.route('/api/photo', methods=['GET'])
def get_photo():
    # Это если хочешь аватарку через бота (но у тебя уже работает photo_url)
    return jsonify({"photo_url": None})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
