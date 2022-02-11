from flask import Flask, config, redirect, request, render_template, jsonify
from discord import SyncWebhook, File
from pathlib import Path
from random import choice
from io import BytesIO

import json

file = Path(__file__).resolve().parent / "tokens.json"
with open(file, 'r') as config_file:
    config_file = json.load(config_file)
    authorization = config_file['authorization']
    vote_webhook_url = config_file['vote_webhook_url']
    patreon_webhook_url = config_file['patreon_webhook_url']

app = Flask(__name__)
VOTE_WEBHOOK = SyncWebhook.from_url(vote_webhook_url)
PATREON_WEBHOOK = SyncWebhook.from_url(patreon_webhook_url)


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/lfg-endpoint", methods=["GET", "POST"])
def receive():
    if request.method == "GET":
        return render_template("405.html")
    if request.headers.get("Authorization") != authorization:
        return
    data = json.loads(request.data)

    VOTE_WEBHOOK.send(f"{data['user']} | {data['guild']}", username="LFG")
    return "OK"


@app.route("/wyr", methods=["GET"])
def wyr():
    wyr_file = Path(r"/home/dan/Task-Manager/cogs/json/WyRQuestionsOld.json")
    with open(wyr_file, "r") as wyr_file:
        wyr_dict = json.load(wyr_file)

    selection = choice(wyr_dict['Questions'])
    try:
        del selection['id']
    except KeyError:
        pass

    return jsonify(selection)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
