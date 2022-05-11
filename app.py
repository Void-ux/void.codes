from flask import Flask, config, redirect, request, render_template, jsonify

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
