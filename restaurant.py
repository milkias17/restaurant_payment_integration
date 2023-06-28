from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy.orm import Session
from sqlalchemy import select

from .db import db_access
from .models import Restaurant

restaurant_bp = Blueprint("restaurant", __name__, url_prefix="/restaurant")


@restaurant_bp.route("/register", methods=["GET", "POST"])
@db_access
def register(db: Session = None):
    if request.method == "POST":
        name = request.form["name"]
        address = request.form["address"]
        phone = request.form["phone"]
        website = request.form["website"]

        for item in [name, address, phone, website]:
            if not item:
                flash("Please fill all fields!")
                return redirect(url_for("restaurant.register"))

        restaurant = Restaurant(name=name, address=address, phone=phone, website=website)
        db.add(restaurant)
        db.commit()
        return redirect(url_for("home"))
    else:
        return render_template("register_restaurant.html")
    


@restaurant_bp.route("/", methods=["GET", "POST"])
@db_access
def list_restaurants(db):
    if request.method == "GET":
        stmt = select(Restaurant).all()
        res = db.scalars(stmt)
        if res:
            return redirect(url_for("home"))
        
    return render_template("register_restaurant.html")



