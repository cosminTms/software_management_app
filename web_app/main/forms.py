from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from flask_login import current_user

from web_app.models import User

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    first_name = StringField('First Name',
                           validators=[DataRequired(),])
    last_name = StringField('Last Name',
                             validators=[DataRequired(), ])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture',
                        validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already exists')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exists')