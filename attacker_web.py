"""Attacker web: serve the page, then open the flip window."""

import os

from flask import Flask, Response, send_from_directory

import phase

ATTACKER_IP = os.environ["ATTACKER_IP"]
PORT = int(os.environ.get("PORT", "8080"))
HERE = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)


@app.get("/")
def index():
    phase.open_local_window()
    return send_from_directory(HERE, "attack.html")


@app.route("/mcp", methods=["GET", "POST"])
@app.route("/mcp/", methods=["GET", "POST"])
def not_yet_rebound():
    return Response('{"rebind":"public"}', mimetype="application/json", headers={"X-Rebind": "public"})


if __name__ == "__main__":
    print(f"[web] http://{ATTACKER_IP}:{PORT}")
    app.run(host=ATTACKER_IP, port=PORT, threaded=True)
