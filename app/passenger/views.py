from flask import Blueprint, redirect, render_template
from flask_login import login_required, current_user
from flask_user import roles_required
pb = Blueprint('passanger_bp',__name__,
			   template_folder='templates',
			   static_folder='app.frontend.static',
			   static_url_path='/static')

from app.models.models import User

@pb.route('/')
@login_required
def home():
	if not User.is_passenger(current_user):
		return redirect('/logout')
	else:
		return render_template('pass_index.html')