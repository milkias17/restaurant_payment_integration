from flask import Blueprint, flash, request, session

from .models import Order

order_bp = Blueprint("order", __name__, url_prefix="/order")


@order_bp.route("/create", methods=["GET", "POST"])
def create_order():
    if request.method == "POST":
        try:
            body = request.get_json()
            food_id = int(body.get("food_id"))
            quantity = int(body.get("quantity"))
            customer_id = int(session.get("customer_id"))

            order = Order(customer_id=customer_id, food_id=food_id, quantity=quantity)
        except Exception:
            flash("Invalid request body!")
