#!/usr/bin/env python3
# Module to define the routes used in the app

from flask import flash, redirect, render_template, url_for

from app.models import User, db
from . import app
from .forms import LoginForm, SignupForm

# app = create_app()  # Create app instance

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login_route():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login_route'))
        else:
            flash('You are now logged in!')
            return redirect(url_for('profile_route'))
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'], strict_slashes=False)
def signup_route():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(firstname=form.firstname.data,
                lastname=form.lastname.data,
                username=form.username.data,
                phonenumber=form.phonenumber.data,
                location=form.location.data,
                gender=form.gender.data,
                email=form.email.data)
        user.set_password(form.password.data)
        user.check_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('profile_route'))
    return render_template('signup.html', form=form)

@app.route('/profile', strict_slashes=False)
def profile_route():
    return render_template('profile.html')
