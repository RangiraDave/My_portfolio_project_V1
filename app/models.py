#!/usr/bin/env python3
# Module to define the models used in the app

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from wtforms import ValidationError


db = SQLAlchemy()
class User(db.Model, UserMixin):
    """Class representing a user in the app."""

    id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), primary_key=True)
    # id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True, nullable=False)
    email = db.Column(db.String(60), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    firstname = db.Column(db.String(32), nullable=False)
    lastname = db.Column(db.String(32), nullable=False)
    gender = db.Column(db.String(10))
    phonenumber = db.Column(db.String(32))
    location = db.Column(db.String(60))

    def set_password(self, password):
        """Set the password for the user."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the user's password."""
        return check_password_hash(self.password_hash, password)
    
    def validate_username(self, username):
        """Validate the uniqueness of the username."""
        user = User.query.filter_by(username=username).first()
        if user is not None:
            raise ValidationError('Username already exists')
        
    def validate_email(self, email):
        """Validate the uniqueness of the email address."""
        user = User.query.filter_by(email=email).first()
        if user is not None:
            raise ValidationError('Email address already exists')
        
    @property
    def is_active(self):
        """Check if the user is active."""
        return True
    
    def get_id(self):
        """Get the user's ID."""
        return self.id

class University(db.Model):
    """Class representing a university in the app."""

    id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), primary_key=True)
    # id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    location = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String(120))
    status = db.Column(db.String(20), default='closed')

class UserPreference(db.Model):
    """Class representing a user's preference in the app."""

    id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), primary_key=True)
    # id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'))
    university_id = db.Column(db.String(36), db.ForeignKey('university.id'))
