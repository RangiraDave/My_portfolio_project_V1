#!/usr/bin/env python3
# Module to initialise the app

from flask import Flask
from flask_login import LoginManager
from flask_mailman import Mail
from flask_migrate import Migrate
from .models import db
# from . import routes


app = Flask(__name__)
app.config['SECRET_KEY'] = 'uruni_urufunguzo_ruhishe'
tp = 'mysql+pymysql://portfolio:Password%40123@localhost/application_copilot'
app.config['SQLALCHEMY_DATABASE_URI'] = tp
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CHATGPT_API_KEY = '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'

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

mail = Mail()
mail.init_app(app)

from app import routes
