from flask import Blueprint

from db import db_access

customer_bp = Blueprint("restaurant", __name__, url_prefix="/restaurant")


@customer_bp.route("/register", methods=["GET", "POST"])
@db_access
def register():
    pass
