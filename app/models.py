#!/usr/bin/env python3
# Module to define the models used in the app

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    gender = db.Column(db.String(10))
    phonenumber = db.Column(db.String(64))
    location = db.Column(db.String(120))  # e.g. country, city

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class University(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    location = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String(120))
    status = db.Column(db.String(20), default='closed')  # open or closed

class UserPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'))