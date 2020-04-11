import os

from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_required, current_user
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

@driveblueprint.route('/')
@login_required
def index():
	if not User.is_driver(current_user):
		return redirect('/logout')
	else:
		return render_template('driver_index.html')

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
				update_user.fullname = form.fullname.data
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
				return render_template('driver_profile_update.html', form=form, imageForm=imageForm, user=user)
		else:
			form.email.data = user.email
			form.fullname.data = user.fullname
			form.zipcode.data = user.zipcode
			form.profiledescription.data = user.profile_description
			return render_template('driver_profile_update.html', form=form, imageForm=imageForm,user=user)


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
		return render_template('driver_profile_update.html', form=form, imageForm=imageForm, user=user)
