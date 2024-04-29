#!/usr/bin/env python3
# Module to define the routes used in the app

from flask import flash, jsonify, redirect, render_template, request, session, url_for
from flask_login import LoginManager, login_user, logout_user, login_manager
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy.exc import IntegrityError
from app.models import University, User, db
# from . import current_app
from . import app, mail, login_manager
from .forms import LoginForm, SignupForm
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_email import Message
from flask_mailman import EmailMessage

# login_manager = LoginManager()
# login_manager.init_app(current_app)

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

s = URLSafeTimedSerializer('ThisisasecretToHelpCreateProtectedTokens!')
# mail = Mail()


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            token = s.dumps(email, salt='email-confirm')
            msg = EmailMessage('Password Reset Request', from_email='noreply@univercityapplicationcopilot.com', to=[email])
            link = url_for('reset_password_with_token', token=token, _external=True)
            print(link)
            msg.body = f'Please follow the password reset link to change your password: {link}'
            mail.send_message(msg)
            flash('A password reset link has been sent to your email.', 'info')
        else:
            flash('Email address not found.', 'warning')
    return render_template('reset_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password_with_token(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except:
        flash('The password reset link is invalid or has expired.', 'warning')
        return redirect(url_for('reset_password'))
    if request.method == 'POST':
        user = User.query.filter_by(email=email).first()
        new_password = request.form['password']
        
        # Password validations
        if len(new_password) < 6:
            flash('Password must be at least 8 characters long.', 'warning')
            return redirect(url_for('reset_password_with_token', token=token))
        if not any(char.isdigit() for char in new_password):
            flash('Password must contain at least one digit.', 'warning')
            return redirect(url_for('reset_password_with_token', token=token))
        if not any(char.isupper() for char in new_password):
            flash('Password must contain at least one uppercase letter.', 'warning')
            return redirect(url_for('reset_password_with_token', token=token))
        if not any(char.islower() for char in new_password):
            flash('Password must contain at least one lowercase letter.', 'warning')
            return redirect(url_for('reset_password_with_token', token=token))
        
        hashed_password = generate_password_hash(new_password, method='sha256')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password_with_token.html')
