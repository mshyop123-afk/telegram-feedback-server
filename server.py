from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


@app.route("/")
def home():
    return "Server is running"


@app.route("/upload", methods=["POST"])
def upload():
    if "photo" not in request.files:
        return jsonify({"error": "photo is required"}), 400

    photo = request.files["photo"]

    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    response = requests.post(
        telegram_url,
        data={"chat_id": CHAT_ID},
        files={"photo": (photo.filename or "win.jpg", photo.stream, photo.mimetype)},
        timeout=30
    )

    return jsonify(response.json()), response.status_code


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
