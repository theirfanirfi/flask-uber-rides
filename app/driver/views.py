import os
from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_required, current_user, confirm_login
from sqlalchemy import text
from werkzeug.utils import secure_filename
from app import application, db
from app.models.models import *

from app.models.models import *
from app.driver.forms import ProfileForm, UploadProfileImageForm
driveblueprint = Blueprint('driver_bp', __name__,
	template_folder='templates',
	static_folder='static',
	static_url_path='assets'
	)

# @application.context_processor
# @login_required
# def inject_dict_for_all_templates():
# 	notifications_count = db.engine.execute("select count(*) from rides where driver_id ="+str(current_user.id)+" and isConfirmed=0 and isStarted = 0 and isPaid = 0 and isEnded =0")
# 	c = str(notifications_count.first()[0])
# 	return dict(count=c)

def get_notifications_count():
	notifications_count = db.engine.execute("select count(*) from rides where driver_id ="+str(current_user.id)+" and isConfirmed=0 and isStarted = 0 and isPaid = 0 and isEnded =0")
	c = str(notifications_count.first()[0])
	return c

@driveblueprint.route('/')
@login_required
def index():
	if not User.is_driver(current_user):
		return redirect('/logout')
	else:
		return render_template('driver_index.html',count=get_notifications_count())


@driveblueprint.route('/profile')
@login_required
def profile():
	user_id = current_user.id
	sql = text(" select *, "
			   "(select count(*) from rides where driver_id = "+str(user_id)+" and isEnded=1) as total_rides, "
			   "(select sum(price) from rides where driver_id = "+str(user_id)+" and isEnded=1) as total_earning "
			   "from users "
			   "LEFT JOIN rides on users.id = rides.driver_id "
			   "WHERE users.id = "+str(user_id)+";")

	user = db.engine.execute(sql)
	u = user.first()

	reviewsFetchSql= text("select *,reviewer.name as reviewer_name from rides LEFT join users as reviewer on reviewer.id = rides.passenger_id "
						  "where rides.driver_id = "+str(user_id)+" and isEnded=1;")
	reviews = db.engine.execute(reviewsFetchSql)

	return render_template('driver_profile.html', user=u, reviews=reviews,count=get_notifications_count())
@driveblueprint.route('/updateprofile', methods=['GET', 'POST'])
@login_required
def update_profile():
	user = current_user
	if not User.is_driver(user):
		return redirect('/logout')
	else:
		form = ProfileForm()
		#form.gender.data = "Male"

		imageForm = UploadProfileImageForm()
		if request.method == "POST":
			if form.validate_on_submit():
				update_user = User.query.filter_by(id=user.id).first()
				update_user.name = form.name.data
				update_user.surname = form.surname.data
				update_user.zipcode = form.zipcode.data
				update_user.gender = form.gender.data
				update_user.email = form.email.data
				update_user.profile_description = form.profiledescription.data
				try:
					db.session.add(update_user)
					db.session.commit()
					flash('Profile Updated')
					return redirect("/driver/updateprofile")
				except Exception as e:
					# return 'Profile not updated '+str(e)
					 flash('Error occurred in updating the profile, please try again.')
					 return redirect("/driver/updateprofile")
			else:
				return render_template('driver_profile_update.html', form=form, imageForm=imageForm, user=user,count=get_notifications_count())
		else:
			form.email.data = user.email
			form.name.data = user.name
			form.surname.data = user.surname
			form.zipcode.data = user.zipcode
			form.profiledescription.data = user.profile_description
			return render_template('driver_profile_update.html', form=form, imageForm=imageForm,user=user,count=get_notifications_count())


@driveblueprint.route("/uploadimage", methods=['POST'])
@login_required
def upload_profile_image():
	form = ProfileForm()
	imageForm = UploadProfileImageForm()
	user = current_user
	form.email.data = user.email
	form.fullname.data = user.fullname
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
			return redirect("/driver/updateprofile")
		except:
			flash('Error occurred in updating the profile image, please try again.')
			return redirect("/driver/updateprofile")
	else:
		return render_template('driver_profile_update.html', form=form, imageForm=imageForm, user=user,count=get_notifications_count())

@driveblueprint.route("/myrides")
@login_required
def my_rides():
	return render_template("driver_my_rides.html",count=get_notifications_count())


@driveblueprint.route("/notifications")
@login_required
def driver_notifications():
	user = current_user
	sql = text("SELECT *,rides.id as ride_id,users.id as p_id,(select count(*) from rides WHERE driver_id = "+str(user.id)+" AND isStarted = 0 AND isConfirmed=0 "
																					  "AND isEnded=0 AND isPaid=0) as total_requests "
																					  "FROM rides LEFT JOIN users on users.id = rides.passenger_id "
			   "WHERE driver_id = "+str(user.id)+" AND isStarted = 0 AND isConfirmed=0 AND isEnded=0 AND isPaid=0;")
	rides = db.engine.execute(sql)

	return render_template("driver_notifications.html", rides=rides, user=user,count=get_notifications_count())

@driveblueprint.route("/approve/<int:request_id>")
@login_required
def approve_request(request_id):
	user = current_user
	ride = Ride.query.filter_by(id=request_id,driver_id=user.id,isConfirmed=0,isStarted=0,isEnded=0).first()
	if not ride:
		return '2' #show alert that no such request found.
	else:
		try:
			ride.isConfirmed = 1
			db.session.add(ride)
			db.session.commit()
			return "1" #request confirmed, please wait for the passenger payment to start the ride.
		except Exception as e:
			return "0" #show alert message, that an error has occurred,request cannot be confirmed. Try refreshing the page

@driveblueprint.route("/decline/<int:request_id>")
@login_required
def decline_request(request_id):
	user = current_user
	ride = Ride.query.filter_by(id=request_id,driver_id=user.id,isConfirmed=0,isStarted=0,isEnded=0).first()
	if not ride:
		return '2' #show alert that no such request found.
	else:
		try:
			ride.isConfirmed = 2 #2 means request declined
			db.session.add(ride)
			db.session.commit()
			return "1" #request declined,
		except Exception as e:
			return "0" #show alert message, that an error has occurred,request cannot be declined. Try refreshing the page



