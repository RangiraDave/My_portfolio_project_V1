#!/usr/bin/env python3
#  Module to initialise the app

from flask import Flask
from flask_migrate import Migrate
from .models import db



app = Flask(__name__)
app.config['SECRET_KEY'] = 'uruni_urufunguzo_ruhishe'
tp = 'mysql+pymysql://portfolio:Password%40123@localhost/application_copilot'
app.config['SQLALCHEMY_DATABASE_URI'] = tp
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.debug = True

db.init_app(app)

migrate = Migrate(app, db)

from . import routes