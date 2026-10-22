import argparse
import os
from pathlib import Path

from flask import Flask, abort, send_from_directory

APP_DIR = Path(__file__).resolve().parent
ASSETS = {"styles.css", "script.js"}
PHOTO_NAMES = {f"darling-{number}.{extension}" for number in range(1, 4) for extension in ("jpg", "jpeg", "png", "webp")}

app = Flask(__name__, static_folder=None)


@app.get("/")
def home():
    return send_from_directory(APP_DIR, "index.html")


@app.get("/<path:filename>")
def asset(filename):
    if filename.startswith("photos/"):
        photo_name = filename.removeprefix("photos/")
        if "/" not in photo_name and photo_name in PHOTO_NAMES:
            return send_from_directory(APP_DIR / "photos", photo_name)
        abort(404)

    if filename not in ASSETS:
        abort(404)
    return send_from_directory(APP_DIR, filename)


def main():
    parser = argparse.ArgumentParser(description="Run the little love web app.")
    parser.add_argument("--host", default=os.environ.get("HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8000")))
    args = parser.parse_args()
    app.run(host=args.host, port=args.port, debug=False)


if __name__ == "__main__":
    main()
