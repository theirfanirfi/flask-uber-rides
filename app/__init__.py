from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


application = Flask(__name__)

# secret key

application.config['SECRET_KEY'] = 'mysecret'

# sql alchemy database
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/ride.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#import models


login_manager = LoginManager()
login_manager.login_view = 'frontend_blue_print.login'
login_manager.init_app(application)

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


