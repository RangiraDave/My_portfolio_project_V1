#!/usr/bin/env python3
# Module to define the models used in the app

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid


db = SQLAlchemy()
class User(db.Model):
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
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class University(db.Model):
    id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), primary_key=True)
    # id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    location = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String(120))
    status = db.Column(db.String(20), default='closed')

class UserPreference(db.Model):
    id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), primary_key=True)
    # id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'))
    university_id = db.Column(db.String(36), db.ForeignKey('university.id'))