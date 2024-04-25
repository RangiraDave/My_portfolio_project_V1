#!/usr/bin/env python3
# Script to create the flask tables from defined models.

from app.models import db
from app import app

with app.app_context():
    db.create_all()
    print('Tables created successfully.')
    exit(0)
