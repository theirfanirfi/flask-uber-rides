from flask import Blueprint, render_template, redirect
from flask_login import login_required,current_user
from app.models.models import *
driveblueprint = Blueprint('driver_bp',__name__,
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

@driveblueprint.route('/updateprofile')
@login_required
def update_profile():
	if not User.is_driver(current_user):
		return redirect('/logout')
	else:
		return render_template('driver_profile_update.html')