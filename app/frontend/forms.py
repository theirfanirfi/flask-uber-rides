# Form Based Imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import DataRequired,Email,EqualTo, Length
from app.models.models import User
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed
# User Based Imports
from flask_login import current_user

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterationForm(FlaskForm):
    fullname = StringField('text',validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Password & Confirm password must match!')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    zipcode = StringField('text',validators=[DataRequired()])
    driver_or_pass = RadioField('Label', choices=[('1', 'Driver'), ('0', 'Passenger')], validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('The entered email is already in use. Please, enter a different one.')
