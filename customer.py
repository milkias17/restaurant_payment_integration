from flask import Blueprint, request, redirect, url_for, render_template
from models import Customer
from db import db_access
from sqlalchemy import select
from sqlalchemy.orm import Session

customer_bp = Blueprint("restaurant", __name__, url_prefix="/restaurant")


@customer_bp.route("/register", methods=["GET", "POST"])
@db_access
def register(db):
    if request.method == "POST":
        name = request.form['name']
        phone = request.form['phone']
        password = request.form['password']
        customer = Customer(name=name, phone=phone, password=password) 
        db.add(customer)
        db.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@customer_bp.route("/login", methods=["GET", "POST"])
@db_access
def login(db: Session):
    if request.method == "POST":
        phone = request.form['phone']
        password = request.form['password']
        stmt = select(Customer).filter_by(phone=phone, password=password)
        res = db.scalars(stmt)
        if res:
            return redirect(url_for('home'))

    return render_template('login.html')

