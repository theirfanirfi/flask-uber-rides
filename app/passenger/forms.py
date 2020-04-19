from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, TextAreaField, HiddenField, IntegerField
from wtforms.validators import DataRequired,Email,EqualTo, Length
from app.models.models import User
from app import application
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_login import current_user
import os

class FindDriverForm(FlaskForm):
    from_loc = StringField('text', validators=[DataRequired()])
    to_loc = StringField('text', validators=[DataRequired()])
    submit = SubmitField('Find Driver')

class BookingRequestForm(FlaskForm):
    from_loc = HiddenField('text', validators=[DataRequired()])
    to_loc = HiddenField('text', validators=[DataRequired()])
    price = HiddenField('text', validators=[DataRequired()])
    distance = HiddenField('text', validators=[DataRequired()])
    submit = SubmitField('Send booking Request')

class PaymentForm(FlaskForm):
    card_number = StringField('text', validators=[DataRequired()])
    cv_code = IntegerField('text', validators=[DataRequired()])
    exp_year = IntegerField('text', validators=[DataRequired()])
    exp_month = IntegerField('text', validators=[DataRequired()])
    payment = IntegerField('text', validators=[DataRequired()])
    driver_id_field = HiddenField('text', validators=[DataRequired()])
    ride_id_field = HiddenField('text', validators=[DataRequired()])
    submit = SubmitField('Pay')

class RideRatingForm(FlaskForm):
    review = TextAreaField('text', validators=[DataRequired()])
    submit = SubmitField('End Ride')

