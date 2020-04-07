from flask import Blueprint, redirect
from flask_login import login_required, current_user
from flask_user import roles_required
pb = Blueprint('passanger_bp',__name__)
from app.models.models import User

@pb.route('/home')
@login_required
def home():
	if not User.is_passenger(current_user):
		return redirect('/logout')
	else:
		return 'passenger index route'