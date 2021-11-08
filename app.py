from flask import Flask, redirect, request, render_template, jsonify
from discord import SyncWebhook
from pathlib import Path
from random import choice

import json

file = Path(__file__).resolve().parent / "tokens.json"
with open(file, 'r') as config_file:
	config_file = json.load(config_file)
	webhook_id = config_file['webhook_id']
	webhook_token = config_file['webhook_token']
	authorization = config_file['authorization']

app = Flask(__name__)
WEBHOOK = SyncWebhook.partial(webhook_id, webhook_token)

@app.route("/")
def hello():
    return render_template("index.html")#"<h1 style='color:blue'>Hello There!</h1>"

@app.route("/lfg-endpoint", methods = ["GET", "POST"])
def receive():
	if request.method == "GET":
		return render_template("405.html")
	if request.headers.get("Authorization") != authorization:
		return
	data = json.loads(request.data)

	WEBHOOK.send(f"{data['user']} | {data['guild']}", username = "LFG")
	return "OK"

@app.route("/taskmanager", methods = ["GET"])
def tm_homepage():
	return render_template("taskmanager.html")

@app.route("/wyr", methods = ["GET"])
def wyr():
	wyr_file = Path(r"/home/dan/TaskManager/cogs/WyRQuestionsOld.json")
	with open (wyr_file, "r") as file:
		file = json.load(file)
	
	selection = choice(file['Questions'])
	try:
		del selection['id']
	except KeyError:
		pass

	return jsonify(selection)

if __name__ == "__main__":
    app.run(host='0.0.0.0')