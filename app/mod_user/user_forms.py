from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField, SelectField, SubmitField
from wtforms.validators import ValidationError, InputRequired, Length, Email, EqualTo
# from app.models import User
from app.models.user import User


class UserForm(FlaskForm):
    fname = StringField('First name', validators=[Length(
        min=2, max=30, message="First name must have length between 2 to 30.")])
    lname = StringField('Last name', validators=[Length(
        min=2, max=30, message="Last name must have length between 2 to 30.")])
    email = StringField('Email', validators=[
        InputRequired("Email is required"), Length(max=100, message="Email should not exceed 100 characters.")])
    password = PasswordField('Password', validators=[
        InputRequired("Password is required"), Length(max=100, message="Password should not exceed 100 characters.")])


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    fname = StringField('First name')
    lname = StringField('Last name')
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    pass_confirm = PasswordField(
        'Confirm password', validators=[InputRequired(), EqualTo(
            'pass_confirm', message='Passwords Must Match!')])
    submit = SubmitField('Register!')

    def validate_email(self, field):
        # Check if not None for that user email!
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def validate_username(self, field):
        # Check if not None for that username!
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')
