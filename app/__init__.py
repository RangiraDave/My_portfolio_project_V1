#!/usr/bin/env python3
# Module to initialise the app

from flask import Flask
from flask_login import LoginManager
from flask_mailman import Mail
from flask_migrate import Migrate
from .models import db
import os
# from . import routes


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'SQLALCHEMY_DATABASE_URI'
    )
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CHATGPT_API_KEY = os.environ.get('CHATGPT_API_KEY')

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

mail = Mail()
mail.init_app(app)

from app import routes

