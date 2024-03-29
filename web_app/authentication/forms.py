from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from werkzeug.security import check_password_hash
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, \
    SelectMultipleField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user

from web_app.models import User, Team, Role


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    role = SelectField('User Role',
                       choices=['Developer', 'Project Manager', 'Chief Technology Officer'],
                       validators = [DataRequired()])
    first_name = StringField('First Name',
                           validators=[DataRequired(),])
    last_name = StringField('Last Name',
                             validators=[DataRequired(), ])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('New User')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

