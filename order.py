from flask import Blueprint, request

order_bp = Blueprint("order", __name__, url_prefix="/order")


@order_bp.route("/create", methods=["GET", "POST"])
def create_order():
    if request.method == "POST":
        pass
