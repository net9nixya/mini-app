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
        "nickname": user[0],
        "elo": user[1],
        "gold": user[2],
        "wins": user[3],
        "losses": user[4],
        "vips": user[5]
    })
