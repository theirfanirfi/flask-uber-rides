from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required
import os
# from flask_cors import CORS


application = Flask(__name__)
# CORS(application)
# secret key
folder = os.path.join(application.root_path,'static/uploads');
application.config['SECRET_KEY'] = 'mysecret'
application.config['UPLOAD_FOLDER'] = folder
# sql alchemy database
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/ride.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#import models

login_manager = LoginManager()

login_manager.login_view = 'frontend_blue_print.login'
login_manager.init_app(application)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

db = SQLAlchemy(application)
from app.models.models import *

#import models


db.create_all()
# Migrate(app, db)


#

from app.frontend.views import fp
from app.driver.views import driveblueprint
from app.passenger.views import pb
application.register_blueprint(pb, url_prefix="/passenger")
application.register_blueprint(driveblueprint, url_prefix="/driver")
application.register_blueprint(fp, url_prefix="/")


