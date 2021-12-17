from flask import Flask, config, redirect, request, render_template, jsonify
from discord import SyncWebhook, webhook, File
from pathlib import Path
from random import choice
from io import BytesIO

import psycopg2
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

conn = psycopg2.connect('dbname=daniel user=daniel')
cur = conn.cursor()

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

	VOTE_WEBHOOK.send(f"{data['user']} | {data['guild']}", username = "LFG")
	return "OK"

@app.route("/lfg-patreon", methods = ["POST"])
def receive_patreon_data():
	data = json.loads(request.data)
	data = json.dumps(data)
	buffer = BytesIO(data.encode('utf8'))
	PATREON_WEBHOOK.send(file = File(fp = buffer, filename = "Traceback.py"))
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