from flask import Blueprint, request, redirect, jsonify, url_for, render_template
from .models import Restaurant, Food
from .db import db_access
from sqlalchemy import select
from sqlalchemy.orm import Session


food_bp = Blueprint("food", __name__, url_prefix="/food")


@food_bp.route("/add", methods=["GET", "POST"])
@db_access
def add(db):
    if request.method == "POST":
        name = request.form['name']
        price = request.form['price']
        restaurant_name = request.form['restaurant_name']

        stmt = select(Restaurant).filter_by(name=restaurant_name)
        restaurant = db.scalars(stmt).first()
        # print(f"Restaurant: {restaurant}")
        if restaurant:
            food = Food(name=name, price=price, restaurant_id=restaurant.id )
            db.add(food)
            db.commit()
            # return jsonify({"test": "hello world"})
        return redirect(url_for("food.add"))

    return render_template('some.html')

@food_bp.route("/foods", methods=["GET", "POST"])
@db_access
def list_foods(db):
    if request.method == "GET":
        restaurant_id = request.args.get("restaurant_id")
        stmt = select(Food).filter_by(restaurant_id=restaurant_id)
        foods = db.scalars(stmt).all()
        if foods:
            return render_template("foods.html", foods=foods)
        
    return redirect(url_for("restaurant.html"))
    

