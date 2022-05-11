from flask import Flask, config, redirect, request, render_template, jsonify
from discord import SyncWebhook, File

app = Flask(__name__)
VOTE_WEBHOOK = SyncWebhook.from_url(vote_webhook_url)
PATREON_WEBHOOK = SyncWebhook.from_url(patreon_webhook_url)


@app.route("/")
def hello():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
