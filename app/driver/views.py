from flask import Blueprint, render_template
from flask_login import login_required
driveblueprint = Blueprint('driver_bp',__name__,
	template_folder='templates',
	static_folder='static',
	static_url_path='assets'
	)

@driveblueprint.route('/home')
@login_required
def index():
	return render_template('index.html')