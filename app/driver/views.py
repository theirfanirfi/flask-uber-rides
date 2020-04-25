import os
from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_required, current_user, confirm_login
from sqlalchemy import text, func
from werkzeug.utils import secure_filename
from app import application, db
from app.models.models import *

from app.models.models import *
from app.driver.forms import ProfileForm, UploadProfileImageForm
from app.passenger.forms import RideRatingForm

driveblueprint = Blueprint('driver_bp', __name__,
                           template_folder='templates',
                           static_folder='static',
                           static_url_path='assets'
                           )


def isDriver():
    user = current_user
    if not user.roles == "Passenger":
        return redirect("/logout")

def has_zipcode_been_updated(user):
    if user.zipcode == 0:
        return True
    else:
        return False


@driveblueprint.route('/')
@login_required
def index():
    user = current_user
    if not User.is_driver(user):
        return redirect('/logout')
    else:
        return render_template('driver_index.html', zipcode_updated=has_zipcode_been_updated(user))


@driveblueprint.route('/profile')
@login_required
def profile():
    isDriver()
    loggedin_user= current_user
    user_id = loggedin_user.id
    total_rides = Ride.query.filter_by(driver_id=loggedin_user.id).count()
    spent = Ride.query.with_entities(func.sum(Ride.price).label('spent')).filter_by(driver_id=loggedin_user.id).all()
    reviews = db.session.query(Ride).join(User, User.id == Ride.driver_id).all()
    return render_template('driver_profile.html', user=loggedin_user, reviews=reviews, zipcode_updated=has_zipcode_been_updated(loggedin_user))


@driveblueprint.route('/updateprofile', methods=['GET', 'POST'])
@login_required
def update_profile():
    isDriver()
    user = current_user
    if not User.is_driver(user):
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
                update_user.email = form.email.data
                update_user.country = form.country.data
                try:
                    db.session.add(update_user)
                    db.session.commit()
                    flash('Profile Updated', 'success')
                    return redirect("/driver/updateprofile")
                except Exception as e:
                    # return 'Profile not updated '+str(e)
                    flash('Error occurred in updating the profile, please try again.','danger')
                    return redirect("/driver/updateprofile")
            else:
                return render_template('driver_profile_update.html', form=form, imageForm=imageForm, user=user,zipcode_updated=has_zipcode_been_updated(user))
        else:
            form.email.data = user.email
            form.name.data = user.name
            form.surname.data = user.surname
            form.zipcode.data = user.zipcode
            form.country.data = user.country
            return render_template('driver_profile_update.html', form=form, imageForm=imageForm, user=user,zipcode_updated=has_zipcode_been_updated(user))


@driveblueprint.route("/uploadimage", methods=['POST'])
@login_required
def upload_profile_image():
    isDriver()
    form = ProfileForm()
    imageForm = UploadProfileImageForm()
    user = current_user
    form.email.data = user.email
    form.name.data = user.name
    form.surname.data = user.surname
    form.zipcode.data = user.zipcode
    form.country.data = user.country
    #form.gender.data = "Male"

    if imageForm.validate_on_submit():
        file = imageForm.image.data
        image = secure_filename(file.filename)
        file_ext = image.split('.')[1]
        if not (file_ext == 'jpeg' or file_ext == 'png' or file_ext == 'jpg'):
            flash('Invalid file, only images can be uploaded','danger')
            return redirect("/driver/updateprofile")

        folder = os.path.join(application.root_path, 'static/uploads/')
        file_path = os.path.join(folder, image)
        try:
            file.save(file_path)
            id = current_user.id
            user = User.query.filter_by(id=id).first()
            user.profile_image = image
            db.session.add(user)
            db.session.commit()
            flash('Profile image Updated','success')
            return redirect("/driver/updateprofile")
        except:
            flash('Error occurred in updating the profile image, please try again.','danger')
            return redirect("/driver/updateprofile")
    else:
        return render_template('driver_profile_update.html', form=form, imageForm=imageForm, user=user,zipcode_updated=has_zipcode_been_updated(user))


@driveblueprint.route("/myrides")
@login_required
def my_rides():
    isDriver()
    user = current_user
    rides = db.engine.execute(text(
        "select *, passenger_ratings as driver_rating_for_pass from rides LEFT join users on users.id = rides.passenger_id "
        "where driver_id = " + str(user.id) + " and isConfirmed=1 and isStarted=1 and isEnded=1"))
    return render_template("driver_my_rides.html",zipcode_updated=has_zipcode_been_updated(user))


@driveblueprint.route("/notifications")
@login_required
def driver_notifications():
    isDriver()
    user = current_user
    sql = text("SELECT *,rides.id as ride_id,users.id as p_id,(select count(*) from rides WHERE driver_id = " + str(
        user.id) + " AND isStarted = 0 AND isConfirmed=0 "
                   "AND isEnded=0 AND isPaid=0) as total_requests "
                   "FROM rides LEFT JOIN users on users.id = rides.passenger_id "
                   "WHERE driver_id = " + str(
        user.id) + " AND isStarted = 0 AND isConfirmed=0 AND isEnded=0 AND isPaid=0;")
    rides = db.engine.execute(sql)

    return render_template("driver_notifications.html", rides=rides, user=user,zipcode_updated=has_zipcode_been_updated(user))


@driveblueprint.route("/approve/<int:request_id>")
@login_required
def approve_request(request_id):
    isDriver()
    user = current_user
    ride = Ride.query.filter_by(id=request_id, driver_id=user.id, isConfirmed=0, isStarted=0, isEnded=0).first()
    if not ride:
        return '2'  # show alert that no such request found.
    else:
        try:
            ride.isConfirmed = 1
            db.session.add(ride)
            db.session.commit()
            return "1"  # request confirmed, please wait for the passenger payment to start the ride.
        except Exception as e:
            return "0"  # show alert message, that an error has occurred,request cannot be confirmed. Try refreshing the page


@driveblueprint.route("/decline/<int:request_id>")
@login_required
def decline_request(request_id):
    isDriver()
    user = current_user
    ride = Ride.query.filter_by(id=request_id, driver_id=user.id, isConfirmed=0, isStarted=0, isEnded=0).first()
    if not ride:
        return '2'  # show alert that no such request found.
    else:
        try:
            ride.isConfirmed = 2  # 2 means request declined
            db.session.add(ride)
            db.session.commit()
            return "1"  # request declined,
        except Exception as e:
            return "0"  # show alert message, that an error has occurred,request cannot be declined. Try refreshing the page


@driveblueprint.route("/started", methods=['GET', 'POST'])
@login_required
def started_ride():
    isDriver()
    user = current_user
    if request.method == 'GET':
        ride = Ride.query.filter_by(driver_id=user.id, isConfirmed=1, isStarted=1, isEnded=0, isPaid=1).first()
        if not ride:
            flash("No started ride found.",'danger')
            return redirect("/driver")

        passenger = User.query.filter_by(id=ride.passenger_id).first()
        if not ride or not passenger:
            return 'No started ride found'  # show alert that no such request found.
        else:
            form = RideRatingForm()
            return render_template('driver_started_ride.html', zipcode_updated=has_zipcode_been_updated(user), ride=ride, user=user,
                                   passenger=passenger, form=form)
    elif request.method == 'POST':
        review = request.form.get('rev')
        stars = request.form.get('str')
        ride_id = request.form.get('id')
        ride = Ride.query.filter_by(driver_id=user.id, id=ride_id, isConfirmed=1, isStarted=1, isPaid=1).order_by(
            Ride.id).first()
        if not ride:
            return "2"  # no such ride found to end
        else:
            ride.driver_review_for_passenger = review
            ride.passenger_ratings = stars
            ride.isEnded = 1
            ride.isReviewedByDriver = 1
            try:
                db.session.add(ride)
                db.session.commit()
                return '1'  # ride ended
            except Exception as e:
                return '0'  # error occurred in reviewing and ending the ride. Try again.
    else:
        return 'Invalid request'


@driveblueprint.route("/zipcode", methods=['GET', 'POST'])
@login_required
def update_zipcode():
    user = current_user
    update_user = User.query.filter_by(id=user.id).first()
    update_user.zipcode = request.args.get('zipcode')
    try:
        db.session.add(update_user)
        db.session.commit()
        flash('Zipcode updated','success')
        return redirect("/driver")
    except:
        flash('Error occurred in updating the zipcode, please try again.')
        return redirect("/driver")