import os

from flask import Flask, send_from_directory

app = Flask(__name__)


@app.get("/")
def invitation():
    return send_from_directory(app.root_path, "index.html")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "5000")),
        debug=False,
    )
