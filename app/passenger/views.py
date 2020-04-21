from flask import Blueprint, redirect, render_template, request, flash
from flask_login import login_required, current_user, confirm_login
from werkzeug.utils import secure_filename
from sqlalchemy import text

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

PRICE = 20


def isPassenger():
    user = current_user
    if not user.roles == "Passenger":
        flash("You are not Driver. Please login/Register with Driver account.")
        return redirect("/logout")


def hasStartedRide(user):
    ride = Ride.query.filter_by(passenger_id=user.id, isConfirmed=1, isPaid=1, isEnded=0).first()
    if ride:
        return True
    else:
        return False

def get_notifications_count():
    notifications_count = db.engine.execute("select count(*) from rides where passenger_id =" + str(
        current_user.id) + " and isConfirmed=1 and isStarted = 0 and isPaid = 0 and isEnded =0")
    c = str(notifications_count.first()[0])
    return c


@pb.route('/')
@login_required
def home():
    user = current_user
    findForm = FindDriverForm()
    if not User.is_passenger(user):
        flash("You are not Driver. Please login/Register with Driver account.")
        return redirect('/logout')
    else:
        rides = db.engine.execute(text(
            "select *, driver_ratings as pass_rating_for_driver from rides LEFT join users on users.id = rides.driver_id "
            "where passenger_id = " + str(user.id) + " and isConfirmed=1 and isStarted=1 and isEnded=1"))
        return render_template('pass_index.html', user=user, form=findForm, count=get_notifications_count(),
                               started_ride=hasStartedRide(user), rides=rides)


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
            flash('please update your zipcode first')
            return redirect(request.referrer)

        drivers = db.engine.execute(text(
            "select *, users.profile_image as driver_profile_image, avg(driver_ratings) as avg_ratings, rides.id as ride_id, users.id as user_driver_id,users.zipcode as driver_zipcode from users LEFT join rides on rides.driver_id = users.id where roles='Driver' and users.zipcode = " + str(
                user.zipcode)))

        if not drivers.scalar():
            drivers = db.engine.execute(text(
                "select *,users.profile_image as driver_profile_image, max(driver_ratings) as top_rated, avg(driver_ratings) as avg_ratings, rides.id as ride_id, users.id as user_driver_id,users.zipcode as driver_zipcode from users LEFT join rides on rides.driver_id = users.id where roles='Driver' and users.zipcode > 0 order by top_rated"))

        return render_template('pass_driver_found.html', drivers=drivers, distance=distance_in_km,
                               price=calculated_price, form=form, from_loc=form.from_loc.data,
                               to_loc=form.to_loc.data, count=get_notifications_count(),
                               started_ride=hasStartedRide(user))


    else:
        flash('please provide the correct locations')
        return redirect(request.referrer)


# return render_template('pass_driver_found.html')

@pb.route('sendbookingreq/<int:driver_id>', methods=['GET', 'POST'])
@login_required
def send_booking_request(driver_id):
    isPassenger()
    from_loc = request.args.get('from_loc')
    to_loc = request.args.get('to_loc')
    price = request.args.get('price')
    distance = request.args.get('distance')
    ride = Ride(driver_id=driver_id, passenger_id=current_user.id, zipcode=current_user.zipcode
                , from_locaton=from_loc, to_location=to_loc, price=price, distance=distance)
    try:
        db.session.add(ride)
        db.session.commit()
        return "1"
    except Exception as e:
        return "0"


@pb.route('/profile')
@login_required
def profile():
    isPassenger()
    user_loggedin = current_user
    user_id = user_loggedin.id
    sql = text(" select *,"
               "(select count(*) from rides where passenger_id = " + str(user_id) + " and isEnded=1) as total_rides,"
                                                                                    "(select sum(price) from rides where passenger_id = " + str(
        user_id) + ") as total_spent "
                   "from users "
                   "LEFT JOIN rides on users.id = rides.passenger_id "
                   "WHERE users.id = " + str(user_id) + ";")

    user = db.engine.execute(sql)
    u = user.first()

    reviewsFetchSql = text(
        "select *,reviewer.name as reviewer_name from rides LEFT join users as reviewer on reviewer.id = rides.driver_id "
        "where rides.passenger_id = " + str(user_id) + ";")
    reviews = db.engine.execute(reviewsFetchSql)
    return render_template('passenger_profile.html', user=u, reviews=reviews, count=get_notifications_count(),
                           started_ride=hasStartedRide(user_loggedin))


@pb.route('/updateprofile', methods=['GET', 'POST'])
@login_required
def update_profile():
    isPassenger()
    user = current_user
    if not User.is_passenger(user):
        return redirect('/logout')
    else:
        form = ProfileForm()
        # form.gender.data = "Male"

        imageForm = UploadProfileImageForm()
        if request.method == "POST":
            if form.validate_on_submit():
                update_user = User.query.filter_by(id=user.id).first()
                update_user.name = form.name.data
                update_user.surname = form.surname.data
                update_user.zipcode = form.zipcode.data
                update_user.country = form.country.data
                update_user.gender = form.gender.data
                update_user.email = form.email.data
                update_user.profile_description = form.profiledescription.data
                try:
                    db.session.add(update_user)
                    db.session.commit()
                    flash('Profile Updated')
                    return redirect("/passenger/updateprofile")
                except Exception as e:
                    # return 'Profile not updated '+str(e)
                    flash('Error occurred in updating the profile, please try again.')
                    return redirect("/passenger/updateprofile")
            else:
                return render_template('driver_profile_update.html', form=form, imageForm=imageForm, user=user,
                                       count=get_notifications_count(), started_ride=hasStartedRide(user))
        else:
            form.email.data = user.email
            form.name.data = user.name
            form.surname.data = user.surname
            form.country.data = user.country
            form.zipcode.data = user.zipcode
            form.profiledescription.data = user.profile_description
            return render_template('passenger_profile_update.html', form=form, imageForm=imageForm, user=user,
                                   count=get_notifications_count())


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
    form.zipcode.data = user.zipcode
    form.gender.data = "Male"

    if imageForm.validate_on_submit():
        file = imageForm.image.data
        image = secure_filename(file.filename)
        folder = os.path.join(application.root_path, 'static/uploads/')
        file_path = os.path.join(folder, image)
        try:
            file.save(file_path)
            id = current_user.id
            user = User.query.filter_by(id=id).first()
            user.profile_image = image
            db.session.add(user)
            db.session.commit()
            flash('Profile image Updated')
            return redirect("/passenger/updateprofile")
        except:
            flash('Error occurred in updating the profile image, please try again.')
            return redirect("/passenger/updateprofile")
    else:
        return render_template('passenger_profile_update.html', form=form, imageForm=imageForm, user=user,
                               count=get_notifications_count(), started_ride=hasStartedRide(user))


@pb.route("/notifications")
@login_required
def passenger_notifications():
    isPassenger()
    user = current_user
    sql = text("SELECT *,rides.id as ride_id,users.id as d_id,(select count(*) from rides WHERE passenger_id = " + str(
        user.id) + " AND isStarted = 0 AND isConfirmed=0 "
                   "AND isEnded=0 AND isPaid=0) as total_requests "
                   "FROM rides LEFT JOIN users on users.id = rides.driver_id "
                   "WHERE passenger_id = " + str(
        user.id) + " AND isStarted = 0 AND isConfirmed=1 AND isEnded=0 AND isPaid=0;")
    rides = db.engine.execute(sql)
    return render_template("passenger_notifications.html", rides=rides, user=user, count=get_notifications_count(),
                           started_ride=hasStartedRide(user))


@pb.route("/pay/<int:ride_id>", methods=['GET', 'POST'])
@login_required
def pay_ride(ride_id):
    isPassenger()
    user = current_user
    ride = Ride.query.filter_by(id=ride_id, passenger_id=user.id, isConfirmed=1, isStarted=0, isEnded=0).first()
    if request.method == 'GET':
        if not ride:
            return 'No such ride found'  # show alert that no such request found.
        else:
            form = PaymentForm()
            form.ride_id_field.data = ride.id
            form.driver_id_field.data = ride.driver_id
            return render_template('pass_pay.html', count=get_notifications_count(), form=form, ride=ride,
                                   started_ride=hasStartedRide(user))
    elif request.method == 'POST':
        ride.isPaid = 1
        ride.isStarted = 1
        try:
            db.session.add(ride)
            db.session.commit()
            return 'ride started'
        except Exception as e:
            return 'error'
        finally:
            decline_all_other_rides = db.engine.execute(
                text("UPDATE rides set isConfirmed=3, isStarted=2 WHERE passenger_id = "
                     + str(user.id) + " and isConfirmed=0 and isEnded=0 and isPaid=0 and isStarted=0;"))
            return redirect("/passenger/started")
    else:
        return 'Invalid request'


@pb.route("/started", methods=['GET', 'POST'])
@login_required
def started_ride():
    isPassenger()
    user = current_user
    ride = Ride.query.filter_by(passenger_id=user.id, isConfirmed=1, isStarted=1, isEnded=0, isPaid=1).first()
    if request.method == 'GET':
        if not ride:
            return 'No started ride found.'
        else:
            driver = User.query.filter_by(id=ride.driver_id).first()
            form = RideRatingForm()
            return render_template('passenger_started_ride.html', count=get_notifications_count(), ride=ride, user=user,
                                   driver=driver, form=form, started_ride=hasStartedRide(user))
    elif request.method == 'POST':
        review = request.form.get('rev')
        stars = request.form.get('str')
        ride_id = request.form.get('id')
        ride = Ride.query.filter_by(passenger_id=user.id, id=ride_id, isConfirmed=1, isStarted=1, isPaid=1).first()
        if not ride:
            return "2"  # no such ride found to end
        else:
            ride.passenger_review_for_driver = review
            ride.driver_ratings = stars
            ride.isEnded = 1
            ride.isReviewedByPassenger = 1
            try:
                db.session.add(ride)
                db.session.commit()
                return '1'  # ride ended
            except Exception as e:
                return '0'  # error occurred in reviewing and ending the ride. Try again.
    else:
        return 'Invalid request'


@pb.route('/myrides')
@login_required
def my_rides():
    isPassenger()
    user = current_user
    rides = db.engine.execute(text(
        "select *, driver_ratings as pass_rating_for_driver from rides LEFT join users on users.id = rides.driver_id "
        "where passenger_id = " + str(user.id) + " and isConfirmed=1 and isStarted=1 and isEnded=1"))
    return render_template('passenger_my_rides.html', rides=rides, count=get_notifications_count(), user=user,
                           started_ride=hasStartedRide(user))
