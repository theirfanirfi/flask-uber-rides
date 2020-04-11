# from flask import mod
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    zipcode = db.Column(db.String(100), nullable=False)
    roles = db.Column(db.String(10), default="Passenger")
    profile_image = db.Column(db.String(255), nullable=True)
    profile_description = db.Column(db.String(255), nullable=True)
    gender = db.Column(db.Integer, nullable=False)
    passengers = db.relationship('Ride', foreign_keys="[Ride.passenger_id]")
    drivers = db.relationship('Ride', foreign_keys="[Ride.driver_id]")

    def __init__(self, name, email, password, zipcode, roles, gender):
        self.fullname = name
        self.email = email
        self.password = generate_password_hash(password)
        self.zipcode = zipcode
        self.roles = roles
        self.gender = gender

    def check_password(self, passw):
        return check_password_hash(self.password, passw)

    def __repr__(self):
        return f"Full name: {self.fullname}"

    def is_driver(user):
        if user.roles == "Driver":
            return True
        else:
            return False

    def is_passenger(user):
        if user.roles == "Passenger":
            return True
        else:
            return False



# from app.models.models import *
# from app import db
# new_user = User(name='Irfan', email='ii@ii.com',password='1234', zipcode='19130', isDriver=0)


class Ride(db.Model):
    __tablename__ = "rides"
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    passenger_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    zipcode = db.Column(db.String(100), nullable=False)
    from_loc = db.Column(db.String(150), nullable=False)
    to_loc = db.Column(db.String(150), nullable=False)
    isStarted = db.Column(db.Integer, default=0)
    isEnded = db.Column(db.Integer, default=0)
    isPaid = db.Column(db.Integer, default=0)
    # will be updated when ride ends
    passenger_ratings = db.Column(db.Integer, nullable=True)
    # will be updated when ride ends
    driver_ratings = db.Column(db.Integer, nullable=True)
    driver_review_for_passenger = db.Column(
        db.String(255), nullable=True)  # will be updated when ride ends
    passenger_review_for_driver = db.Column(
        db.String(255), nullable=True)  # will be updated when ride ends
    price = db.Column(db.Integer, nullable=False)

    def __init__(self, driver, passenger, zipcode, from_locaton, to_location, ispaid, price):
        self.driver_id = driver
        self.passenger_id = passenger
        self.zipcode = zipcode
        self.from_loc = from_locaton
        self.to_loc = to_location
        self.isPaid = ispaid
        self.price = price
