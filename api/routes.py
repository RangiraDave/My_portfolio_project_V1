#!/usr/bin/env python3
""" Module for api routes. """

from flask import jsonify, request
from flask_login import login_required
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash
import app
from app.models import University, User, UserPreference


s = URLSafeTimedSerializer('ThisisasecretToHelpCreateProtectedTokens!')

@app.route('/api/signup', methods=['POST'], strict_slashes=False)
def signup():
    """ Route for signing up a user. """
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    firstname = data.get('firstname')
    lastname = data.get
    user = User(
        email=email,
        username=username,
        firstname=firstname,
        lastname=lastname
        )
    app.db.session.add(user)
    app.db.session.commit()
    return jsonify({'message': 'User signed up successfully'}), 201

@app.route('/api/login', methods=['POST'], strict_slashes=False)
@login_required
def login():
    """ Route for logging in a user. """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        return jsonify({'message': 'Invalid email or password'}), 401
    return jsonify({'message': 'User logged in successfully'}), 200

@app.route('/api/universities', methods=['GET'], strict_slashes=False)
def universities():
    """ Route for getting all universities. """
    # University.query.all()
    universities = University.query.all()
    return jsonify({'universities': [
        university.to_dict() for university in universities
        ]}), 200

@app.route('/api/universities/<id>', methods=['GET'], strict_slashes=False)
def university(id):
    """ Route for getting a university by id. """
    University.query.filter_by(id=id).first()
    return jsonify({'message': 'University returned successfully'}), 200

@app.route('/api/universities', methods=['POST'], strict_slashes=False)
def add_university():
    """ Route for adding a university. """
    data = request.get_json()
    name = data.get('name')
    location = data.get('location')
    website = data.get('website')
    status = data.get('status')
    university = University(
        name=name, location=location,
        website=website, status=status
        )
    app.db.session.add(university)
    app.db.session.commit()
    return jsonify({'message': 'University added successfully'}), 201

@app.route('/api/universities/<id>', methods=['PUT'], strict_slashes=False)
def update_university(id):
    """ Route for updating a university. """
    data = request.get_json()
    name = data.get('name')
    location = data.get('location')
    website = data.get('website')
    status = data.get('status')
    university = University.query.filter_by(id=id).first()
    university.name = name
    university.location = location
    university.website = website
    university.status = status
    return jsonify({'message': 'University updated successfully'}), 200

@app.route('/api/users/<id>', methods=['DELETE'], strict_slashes=False)
def user(id):
    """ Route for deleting a user if exists. """
    if User.query.filter_by(id=id).first() is None:
        return jsonify({'message': 'User not found'}), 404
    User.query.filter_by(id=id).delete()
    return jsonify({'message': 'User deleted successfully'}), 200

@app.route('/api/user', methods=['GET'], strict_slashes=False)
def user():
    """ Route for getting a user by id. """
    User.query.all()
    return jsonify({'message': 'User returned successfully'}), 200

@app.route('/api/user_priferences/<id>', methods=['GET'], strict_slashes=False)
def user_preferences(id):
    """ Route for getting a user preferences by id. """
    if UserPreference.query.filter_by(id=id).first() is None:
        return jsonify({'message': 'User preferences not found'}), 404
    UserPreference.query.filter_by(id=id).first()
    return jsonify({'message': 'User preferences returned successfully'}), 200

@app.route('/api/reset_password', methods=['POST'], strict_slashes=False)
def reset_password():
    """ Route for resetting a user password. """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user.password = generate_password_hash(password)
    app.db.session.commit()
    return jsonify({'message': 'Password reset successfully'}), 200

@app.route('/api/reset_password/<token>', methods=['POST'], strict_slashes=False)
def reset_password(token):
    """ Route for resetting a user password. """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    return jsonify({'message': 'Password reset successfully'}), 200
