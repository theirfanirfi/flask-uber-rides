from flask import Blueprint, render_template, request, flash, redirect
from app.frontend.forms import LoginForm, RegisterationForm
from flask_login import login_user, current_user, logout_user, login_required
fp = Blueprint('frontend_blue_print', __name__,
               template_folder='templates',
               static_folder='app.frontend.static',
               static_url_path='/static')
from app.models.models import User
from app import db


@fp.route('/')
def index():
    return render_template('index.html')


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

            user = User(name=form.fullname.data,email=form.email.data,password=form.password.data,
                        zipcode=form.zipcode.data,roles=role,gender=form.gender.data)
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
