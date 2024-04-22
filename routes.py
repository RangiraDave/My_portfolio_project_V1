from flask import render_template
from . import create_app


app = create_app()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login', strict_slashes=False)
def login_route():
    return render_template('login.html')

@app.route('/signup', strict_slashes=False)
def signup_route():
    return render_template('signup.html')

@app.route('/profile', strict_slashes=False)
def profile_route():
    return render_template('profile.html')
