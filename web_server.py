#!/usr/bin/env python3
"""
Простой веб-сервер для healthcheck на хостинге
"""

import os

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def health_check():
    """Health check endpoint для хостинга"""
    return jsonify(
        {"status": "healthy", "service": "Jawa CZ Telegram Bot", "version": "1.0.0"}
    )


@app.route("/health")
def health():
    """Дополнительный health check"""
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    app.run(host="0.0.0.0", port=port)
