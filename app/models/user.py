"""Models and database functions for this app."""
from flask_login import UserMixin
from typing import List
from app.db import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    """User model. Inherits UserMixin to get access to
    is_authenticated(), is_active(), is_anonymous(), get_id() which we will
    call in our app routes.
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(30), nullable=True)
    lname = db.Column(db.String(30), nullable=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), nullable=False, index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        """User info"""
        return f'<User id={self.id} username={self.username} email={self.email}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
