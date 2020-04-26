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
    return render_template('index.html')


@fp.route('login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if not user:
                flash('Invalid Credentials','danger')
                return redirect("/login")
            if user.check_password(form.password.data) and user is not None:
                login_user(user)
                if (not user.zipcode == 0 and not user.roles == 'Passenger'):
                    flash('','zipcode')

                if user.roles == "Driver":
                    return redirect('/driver')
                else:
                    return redirect('/passenger')
            else:
                flash('Invalid Credentials','danger')
                return redirect("/login")
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
    if request.method == 'GET':
        return render_template('register.html',form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            if form.driver_or_pass.data=="0":
                role = "Passenger"
            else:
                role = "Driver"

            user = User(name=form.name.data,surname=form.surname.data,email=form.email.data,country=form.country.data,password=form.password.data,roles=role)
            db.session.add(user)
            try:
                db.session.commit()
                flash('Registeration successful, please login to continue.','success')
                return redirect("/login")
            except:
                flash('Error occurred during registeration. Please try again.','danger')
                return redirect(request.referrer)
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
