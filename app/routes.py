#!/usr/bin/env python3
# Module to define the routes used in the app

from flask import flash, jsonify, redirect, render_template, request, session, url_for
from flask_login import LoginManager, login_user, logout_user
from sqlalchemy.exc import IntegrityError
from app.models import University, User, db
from . import app
from .forms import LoginForm, SignupForm
from werkzeug.security import generate_password_hash, check_password_hash


login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/', strict_slashes=False)
def index():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login_route():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            session['email'] = form.email.data
            flash('You are now logged in!')
            print('You are now logged in!')
            return redirect(url_for('profile_route'))
        else:
            flash('Invalid email or password')
            print('Invalid email or password')
            return redirect(url_for('login_route'))
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'], strict_slashes=False)
def signup_route():
    form = SignupForm()
    if form.validate_on_submit():
        user_exists = User.query.filter_by(username=form.username.data).first()
        if user_exists:
            flash('Username already exists. Please choose a different one.', 'error')
            return redirect(url_for('signup_route'))

        user = User(firstname=form.firstname.data,
                lastname=form.lastname.data,
                username=form.username.data,
                phonenumber=form.phonenumber.data,
                location=form.location.data,
                gender=form.gender.data,
                email=form.email.data)
        user.set_password(form.password.data)

        db.session.add(user)
        try:
            db.session.commit()
            session['email'] = form.email.data
            flash('Account created successfully!')
            return redirect(url_for('profile_route'))
        except IntegrityError:
            db.session.rollback()
            flash('Email already exists')
            return redirect(url_for('signup_route'))
    return render_template('signup.html', title='signup', form=form)

@app.route('/profile', strict_slashes=False)
def profile_route():
    """
    A method to fetch data from the database and display it on
    the profile page.
    """
    if 'email' not in session:
        return redirect(url_for('login_route'))
    
    user = User.query.filter_by(email=session['email']).first()
    return render_template(
        'profile.html',
        username=user.username,
        email=user.email,
        phone=user.phonenumber,
        location=user.location
        )

@app.route('/check_email', methods=['GET'], strict_slashes=False)
def check_email():
    """ Check if email being used to login exists in the database. """
    email = request.args.get('email', '', type=str)
    user = User.query.filter_by(email=email).first()
    return jsonify({'exists': user is not None})

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/signup', methods=['GET', 'POST'], strict_slashes=False)
def signup():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Registered sucessfully!'})

@app.route('/login', methods=['POST'], strict_slashes=False)
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        login_user(user)
        return jsonify({'message': 'Logged in successfully!'})
    return jsonify({'message': 'Invalid email or password'})

@app.route('/logout', strict_slashes=False)
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully!'})

@app.route('/account_recovery', strict_slashes=False)
def account_recovery():
    return jsonify({'message': 'Account recovery page'})
@app.route('/universities', methods=['GET'], strict_slashes=False)
def get_universities():
    universities = University.query.all()
    # def to_dict(self):
    #     return {
    #         'id': self.id,
    #         'name': self.name,
    #         'location': self.location,
    #         'website': self.website,
    #         'status': self.status
    #     }
    return jsonify([university.serialize() for university in universities])
