from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello World!"


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        return "You are registered!"
