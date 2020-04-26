from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, HiddenField, IntegerField, SelectField
from wtforms.validators import DataRequired,Email,EqualTo, Length, NumberRange, InputRequired
from app.models.models import User
from app import application
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_login import current_user
import os

class FindDriverForm(FlaskForm):
    from_loc = IntegerField('Number', validators=[NumberRange(min=10121,max=10156,message='Invalid zipcode')])
    to_loc = IntegerField('Number', validators=[NumberRange(min=10121,max=10156,message='Invalid zipcode')])
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
    payment = HiddenField('Number', validators=[DataRequired()])
    driver_id_field = HiddenField('Number', validators=[DataRequired()])
    distance_field = HiddenField('Number', validators=[DataRequired()])
    start_zipcode = HiddenField('Number', validators=[DataRequired()])
    end_zipcode = HiddenField('Number', validators=[DataRequired()])
    submit = SubmitField('Pay')

class RideRatingForm(FlaskForm):
    review = TextAreaField('text', validators=[DataRequired()])
    stars = SelectField('Rating', coerce=int, choices=[(1,"1 Star"),(2,"2 Stars"), (3, '3 stars'), (4, '4 stars'), (5, '5 Stars')], validators=[DataRequired()])
    ride_id = HiddenField('Number', validators=[DataRequired()])
    submit = SubmitField('End Ride')

