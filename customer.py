from flask import Blueprint, redirect, render_template, request, session, url_for
from sqlalchemy import select
from sqlalchemy.orm import Session

from .db import db_access
from .models import Customer

customer_bp = Blueprint("customer", __name__, url_prefix="/customer")


@customer_bp.route("/register", methods=["GET", "POST"])
@db_access
def register(db):
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        password = request.form["password"]
        customer = Customer(name=name, phone=phone, password=password)
        db.add(customer)
        db.commit()
        return redirect(url_for("customer.login"))
    return render_template("signUp.html")


@customer_bp.route("/login", methods=["GET", "POST"])
@db_access
def login(db: Session):
    if request.method == "POST":
        phone = request.form["phone"]
        password = request.form["password"]
        stmt = select(Customer).filter_by(phone=phone, password=password)
        res = db.scalars(stmt).first()
        if res:
            session["customer_id"] = res.id
            return redirect(url_for("home"))

    return render_template("loginPage.html")
