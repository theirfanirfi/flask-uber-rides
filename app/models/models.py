from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    country = db.Column(db.String(100),nullable=True)
    password = db.Column(db.String(150), nullable=False)
    zipcode = db.Column(db.Integer, default=0)
    roles = db.Column(db.String(10), default="Passenger")
    profile_image = db.Column(db.String(255), nullable=True, default="0")
    profile_description = db.Column(db.String(255), nullable=True)
    gender = db.Column(db.Integer, nullable=False)
    member_since = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    charges_per_kilo = db.Column(db.Integer, default=0) #only for driver
    passengers = db.relationship('Ride', foreign_keys="[Ride.passenger_id]")
    drivers = db.relationship('Ride', foreign_keys="[Ride.driver_id]")

    def __init__(self, name, surname, email, password, roles, gender):
        self.name = name
        self.surname = surname
        self.email = email
        self.password = generate_password_hash(password)
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
    zipcode = db.Column(db.Integer, nullable=False)
    from_loc = db.Column(db.String(150), nullable=False)
    to_loc = db.Column(db.String(150), nullable=False)
    isStarted = db.Column(db.Integer, default=0) #0: not started, 1: started, 2: responded by other driver.
    isEnded = db.Column(db.Integer, default=0) #0: not ended, 1: ended
    isPaid = db.Column(db.Integer, default=0) #0: not paid, 1: paid
    isConfirmed = db.Column(db.Integer, default=0) #0: request not entertained yet, 1: accepted, 2: declined, 3: repsonded by other driver.
    # will be updated when ride ends
    passenger_ratings = db.Column(db.Integer, nullable=True)
    # will be updated when ride ends
    driver_ratings = db.Column(db.Integer, nullable=True)
    passenger_ratings = db.Column(db.Integer, nullable=True)
    distance = db.Column(db.Integer, nullable=False)
    driver_review_for_passenger = db.Column(
        db.String(255), nullable=True)  # will be updated when ride ends
    passenger_review_for_driver = db.Column(
        db.String(255), nullable=True)  # will be updated when ride ends
    price = db.Column(db.Integer, nullable=False)
    isReviewedByDriver = db.Column(db.Integer, nullable=False, default=0)
    isReviewedByPassenger = db.Column(db.Integer, nullable=False, default=0)
    ride_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, driver_id, passenger_id, zipcode, from_locaton, to_location, price,distance):
        self.driver_id = driver_id
        self.passenger_id = passenger_id
        self.zipcode = zipcode
        self.from_loc = from_locaton
        self.to_loc = to_location
        self.price = price
        self.distance = distance
