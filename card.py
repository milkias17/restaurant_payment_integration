from flask import Blueprint, flash, redirect, render_template, request, url_for, session
from sqlalchemy.orm import Session
from sqlalchemy import select
from .order import order_bp
from .db import db_access
from .models import Order, Customer

restaurant_bp = Blueprint("orders", __name__, url_prefix="/orders")


@order_bp.route("/orders", methods=["GET"])
@db_access
def list_orders(db):

    if session.get("Customer_id"):
        customer_id = session["Customer_id"]
        stmt = select(Order).filter_by(customer_id=customer_id).all()
        orders = db.scalars(stmt).all()
        total = 0
        for order in orders:
            total += orders.price

        render_template("list.html", orders=orders, total=total)

        




