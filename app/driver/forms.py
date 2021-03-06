from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired,Email,EqualTo, Length, Regexp
from app.models.models import User
from app import application
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_login import current_user
import os
# from flask_uploads import UploadSet, IMAGES
#
# images = UploadSet('images', IMAGES)

class ProfileForm(FlaskForm):
    name = StringField('text',validators=[DataRequired()])
    surname = StringField('text',validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    country = StringField('Country', validators=[DataRequired()])
    zipcode = IntegerField('Number')
    submit = SubmitField('Update Profile')

    def validate_email(self, field):
        if not current_user.email == field.data and User.query.filter_by(email=field.data).first():
            raise ValidationError("The email is already taken")

class UploadProfileImageForm(FlaskForm):
    image = FileField(validators=[FileRequired()])
    submit = SubmitField('Upload Profile Image')

    # def validate_image(self, field):
    #     folder = os.path.join(application.root_path, 'static/uploads/')
    #     file_path = os.path.join(folder, field.data.filename)
    #     if os.path.isfile(file_path):
    #         raise ValidationError("Image with the same name already exists.")

class ZipCodeForm(FlaskForm):
    zipcode = IntegerField('number',validators=[DataRequired(), Regexp(regex=r'^\d+$')])
    submit = SubmitField('Update')
