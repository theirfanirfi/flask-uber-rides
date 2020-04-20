from flask import Blueprint, render_template, request, flash, redirect
from app.frontend.forms import LoginForm, RegisterationForm
from flask_login import login_user, current_user, logout_user, login_required
fp = Blueprint('frontend_blue_print', __name__,
               template_folder='templates',
               static_folder='app.frontend.static',
               static_url_path='/static')
from app.models.models import User
from app import db
from app.passenger.forms import *
from sqlalchemy import text

@fp.route('/')
def index():
    findform = FindDriverForm()
    return render_template('index.html', form=findform)


@fp.route('login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user.check_password(form.password.data) and user is not None:
                login_user(user)
                flash('You are logged in. ')
                if user.roles == "Driver":
                    return redirect('/driver')
                else:
                    return redirect('/passenger')
            else:
                return 'Invalid credentials'
        else:
            return render_template('login.html', form=form)
    elif request.method == 'GET':
        return render_template('login.html',form=form)
    else:
        return 'error'

@fp.route('register', methods=['GET', 'POST'])
def register():
    form = RegisterationForm()
    role = "Passenger"
    gender= ""
    if request.method == 'GET':
        return render_template('register.html',form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            if form.driver_or_pass.data=="0":
                role = "Passenger"
            else:
                role = "Driver"

            user = User(name=form.name.data,surname=form.surname.data,email=form.email.data,password=form.password.data,roles=role,gender=form.gender.data)
            db.session.add(user)
            try:
                db.session.commit()
                return 'Thank you for registeration. Please go to login page and login.'
            except:
                return 'Error occurred during registeration. Please try again.'
        else:
            # return 'not validate'
            return render_template('register.html', form=form)
    else:
        return render_template('register.html',form=form)

@fp.route('logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")

@fp.route('driver/<int:driver_id>')
def driver_profile(driver_id):
    sql = text(" select *, users.zipcode as driver_zipcode, "
               "(select count(*) from rides where driver_id = " + str(driver_id) + " and isEnded=1) as total_rides, "
                                                                                 "(select sum(price) from rides where driver_id = " + str(
        driver_id) + " and isEnded=1) as total_earning "
                   "from users "
                   "LEFT JOIN rides on users.id = rides.driver_id "
                   "WHERE users.id = " + str(driver_id) + " and roles='Driver'")

    user = db.engine.execute(sql)
    u = user.first()

    reviewsFetchSql = text(
        "select *,reviewer.name as reviewer_name,  rides.driver_ratings as d_ratings from rides LEFT join users as reviewer on reviewer.id = rides.passenger_id "
        "where rides.driver_id = " + str(driver_id) + " and isEnded=1;")
    reviews = db.engine.execute(reviewsFetchSql)
    return render_template("frontend_driver_profile.html", user=u, reviews=reviews)



@fp.route('passenger/<int:passenger_id>')
def passenger_profile(passenger_id):
    sql = text(" select *, users.zipcode as driver_zipcode,"
               "(select count(*) from rides where passenger_id = " + str(passenger_id) + " and isEnded=1) as total_rides, "
                                                                                 "(select sum(price) from rides where passenger_id = " + str(
        passenger_id) + " and isEnded=1) as total_spent "
                   "from users "
                   "LEFT JOIN rides on users.id = rides.passenger_id "
                   "WHERE users.id = " + str(passenger_id) + " and roles='Passenger'")

    user = db.engine.execute(sql)
    u = user.first()

    reviewsFetchSql = text(
        "select *,reviewer.name as reviewer_name, rides.passenger_ratings as p_ratings from rides LEFT join users as reviewer on reviewer.id = rides.driver_id "
        "where rides.passenger_id = " + str(passenger_id) + " and isEnded=1;")
    reviews = db.engine.execute(reviewsFetchSql)
    return render_template("frontend_passenger_profile.html", user=u, reviews=reviews)
