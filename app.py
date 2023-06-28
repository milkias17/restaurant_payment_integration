from flask import Flask, request

from .db import init_db
from .restaurant import restaurant_bp

init_db()

app = Flask(__name__)
app.register_blueprint(restaurant_bp)


@app.route("/")
def home():
    return "Hello World!"


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        return "You are registered!"
