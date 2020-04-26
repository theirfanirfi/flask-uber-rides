from flask import Blueprint, redirect, render_template, request, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from sqlalchemy import text, func


pb = Blueprint('passenger_bp', __name__,
               template_folder='templates',
               static_folder='app.frontend.static',
               static_url_path='/static')

from app.models.models import User
from app.passenger.forms import *
from app.driver.forms import *
from random import randint
from app.models.models import *
from app import db
import sys

PRICE = 20


def isPassenger():
    user = current_user
    if not user.roles == "Passenger":
        flash("You are not Driver. Please login/Register with Driver account.", 'danger')
        return redirect("/logout")


@pb.route('/')
@login_required
def home():
    user = current_user
    findForm = FindDriverForm()
    if not User.is_passenger(user):
        flash("You are not a Driver. Please login/Register with Driver account.", 'danger')
        return redirect('/logout')
    else:
        rides = db.engine.execute(text("SELECT * from rides left join users on users.id = rides.driver_id where passenger_id = "+str(user.id)))
        return render_template('pass_index.html', user=user, form=findForm, rides=rides)


@pb.route('find', methods=['POST'])
@login_required
def finddriver():
    isPassenger()
    form = FindDriverForm()
    distance_in_km = randint(1, 51)
    calculated_price = distance_in_km * PRICE
    stars = 3
    drivers = ''
    user = current_user
    if form.validate_on_submit():
        if not int(user.zipcode) > 0:
            flash('please update your zipcode first', 'warning')
            return redirect(request.referrer)

        passenger_zipcode = form.from_loc.data
        s1 = User.query.filter(User.roles == 'Driver', User.zipcode >= form.from_loc.data)
        s2 = User.query.filter(User.roles == 'Driver', User.zipcode <= form.to_loc.data)
        drivers = s1.union(s2).order_by(User.zipcode.asc())

        closest_drivers = []
        minimum = sys.maxsize  # Largest possible integer in Python

        for d in drivers:  # Finds the shortest distance
            distance = abs(d.zipcode - passenger_zipcode)
            if distance < minimum:
                minimum = distance

        for d in drivers:  # Get list of drivers who are at the shortest distance
            distance = abs(d.zipcode - passenger_zipcode)
            if distance == minimum:
                closest_drivers.append(d)

        return render_template('pass_driver_found.html', drivers=closest_drivers, distance=distance_in_km,
                               price=calculated_price, form=form, from_loc=form.from_loc.data,
                               to_loc=form.to_loc.data, start_zipcode=form.from_loc.data, end_zipcode=form.to_loc.data)


    else:
        return render_template('pass_index.html', form=form)


# return render_template('pass_driver_found.html')


@pb.route('/profile')
@login_required
def profile():
    isPassenger()
    user = current_user
    user_id = user.id

    total_rides = Ride.query.filter_by(passenger_id=user_id).count()
    spent = Ride.query.with_entities(func.sum(Ride.price).label('spent')).filter_by(passenger_id=user_id).all()[0][0]
    return render_template('passenger_profile.html', user=user, spent=spent, total_rides=total_rides)


@pb.route('/updateprofile', methods=['GET', 'POST'])
@login_required
def update_profile():
    isPassenger()
    user = current_user
    if not User.is_passenger(user):
        return redirect('/logout')
    else:
        form = ProfileForm()
        imageForm = UploadProfileImageForm()
        if request.method == "POST":
            if form.validate_on_submit():
                update_user = User.query.filter_by(id=user.id).first()
                update_user.name = form.name.data
                update_user.surname = form.surname.data
                update_user.country = form.country.data
                update_user.email = form.email.data
                try:
                    db.session.add(update_user)
                    db.session.commit()
                    flash('Profile Updated', 'success')
                    return redirect("/passenger/updateprofile")
                except Exception as e:
                    # return 'Profile not updated '+str(e)
                    flash('Error occurred in updating the profile, please try again.', 'danger')
                    return redirect("/passenger/updateprofile")
            else:
                return render_template('driver_profile_update.html', form=form, imageForm=imageForm, user=user)
        else:
            form.email.data = user.email
            form.name.data = user.name
            form.surname.data = user.surname
            form.country.data = user.country
            return render_template('passenger_profile_update.html', form=form, imageForm=imageForm, user=user)


@pb.route("/uploadimage", methods=['POST'])
@login_required
def upload_profile_image():
    isPassenger()
    form = ProfileForm()
    imageForm = UploadProfileImageForm()
    user = current_user
    form.email.data = user.email
    form.name.data = user.name
    form.surname.data = user.surname

    if imageForm.validate_on_submit():
        file = imageForm.image.data
        image = secure_filename(file.filename)
        file_ext = image.split('.')[1]
        if not (file_ext == 'jpeg' or file_ext == 'png' or file_ext == 'jpg'):
            flash('Invalid file, only images can be uploaded', 'danger')
            return redirect("/passenger/updateprofile")

        folder = os.path.join(application.root_path, 'static/uploads/')
        file_path = os.path.join(folder, image)
        try:
            file.save(file_path)
            id = current_user.id
            user = User.query.filter_by(id=id).first()
            user.profile_image = image
            db.session.add(user)
            db.session.commit()
            flash('Profile image Updated', 'success')
            return redirect("/passenger/updateprofile")
        except:
            flash('Error occurred in updating the profile image, please try again.', 'danger')
            return redirect("/passenger/updateprofile")
    else:
        return render_template('passenger_profile_update.html', form=form, imageForm=imageForm, user=user)


@pb.route("/started", methods=['GET', 'POST'])
@login_required
def started_ride():
    isPassenger()
    user = current_user
    form = RideRatingForm()
    ride = Ride.query.filter_by(passenger_id=user.id, isStarted=1, isEnded=0, isPaid=1).first()
    if request.method == 'GET':
        if not ride:
            flash('No started ride found', 'danger')
            return redirect(request.referrer)
        else:
            driver = User.query.filter_by(id=ride.driver_id).first()
            form.ride_id.data = ride.id
            return render_template('passenger_started_ride.html', ride=ride, user=user,
                                   driver=driver, form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            review = form.review.data
            stars = form.stars.data
            ride_id = form.ride_id.data
            ride = Ride.query.filter_by(passenger_id=user.id, id=ride_id, isStarted=1, isPaid=1).first()
            if not ride:
                flash('No such ride found to review', 'danger')
                return redirect(request.referrer)
            else:
                ride.passenger_review_for_driver = review
                ride.driver_ratings = stars
                ride.isEnded = 1
                ride.isReviewedByPassenger = 1
                try:
                    db.session.add(ride)
                    db.session.commit()
                    flash('Ride ended', 'success')
                    return redirect('/passenger')
                except Exception as e:
                    flash('Error occurred, please try again', 'danger')
                    return redirect(request.referrer)
        else:
            flash('Invalid review','danger')
            return redirect(request.referrer)
    else:
        return 'Invalid request'


@pb.route('/myrides')
@login_required
def my_rides():
    isPassenger()
    user = current_user
    rides = db.engine.execute(text("SELECT * from rides left join users on users.id = rides.driver_id where passenger_id = " + str(user.id)))
    return render_template('passenger_my_rides.html', rides=rides, user=user, )


@pb.route('/start', methods=['GET', 'POST'])
@login_required
def start_ride():
    form = PaymentForm()
    user = current_user
    if request.method == "GET":
        distance = request.args.get('distance')
        start_zipcode = request.args.get('start_zipcode')
        end_zipcode = request.args.get('end_zipcode')
        if not (int(start_zipcode) >= 10121 and int(start_zipcode) <= 10156) and not (
                int(end_zipcode) >= 10121 and int(end_zipcode) <= 10156):
            flash('Invalid zipcodes provided.', 'danger')
            return redirect(request.referrer)

        driver_id = request.args.get('driver_id')
        price = request.args.get('price')
        form.start_zipcode.data = start_zipcode
        form.end_zipcode.data = end_zipcode
        form.driver_id_field.data = driver_id
        form.distance_field.data = distance
        form.payment.data = price
        return render_template('pass_pay.html', form=form, price=price)
    elif request.method == "POST":
        if form.validate_on_submit():
            ride = Ride(driver_id=form.driver_id_field.data, passenger_id=user.id, zipcode=1234,
                        from_locaton=form.start_zipcode.data, to_location=form.end_zipcode.data,
                        price=form.payment.data, distance=form.distance_field.data, isPaid=1, isStarted=1)
            try:
                db.session.add(ride)
                db.session.commit()
                flash('Ride started', 'success')
                return redirect("/passenger/started")
            except:
                flash('Error occurred in starting the ride, please try again', 'danger')
                return redirect(request.referrer)
        else:
            flash('Please fill in the form correctly.', 'danger')
            return redirect(request.referrer)
    else:
        flash('Invalid request method', 'danger')
        return redirect(request.referrer)
