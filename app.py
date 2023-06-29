from flask import Flask, request

from .customer import customer_bp
from .db import init_db
from .restaurant import restaurant_bp
from .food import food_bp
from .customer import customer_bp
from .order import order_bp

init_db()

app = Flask(__name__)
app.secret_key = "Jzg+4jm8V11jDeexvVRTyUl4yQUM9BN6kYMP4j+8Wd/GBKaUUkpwI1uhy9vW6BrZ"
app.register_blueprint(restaurant_bp)
app.register_blueprint(food_bp)
app.register_blueprint(customer_bp)
app.register_blueprint(order_bp)

@app.route("/")
def home():
    return "Hello World!"


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        return "You are registered!"
