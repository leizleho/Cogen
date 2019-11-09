from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField, SelectField
from wtforms.validators import InputRequired, Length


class UserForm(FlaskForm):
    fname = StringField('First name', validators=[Length(
        min=2, max=30, message="First name must have length between 2 to 30.")])
    lname = StringField('Last name', validators=[Length(
        min=2, max=30, message="Last name must have length between 2 to 30.")])
    email = StringField('Email', validators=[
        InputRequired("Email is required"), Length(max=100, message="Email should not exceed 100 characters.")])
    password = PasswordField('Password', validators=[
        InputRequired("Password is required"), Length(max=100, message="Password should not exceed 100 characters.")])
