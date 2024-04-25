#!/usr/bin/env python3
# Module to define the forms used in the app

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField
from wtforms import SubmitField, ValidationError
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    phonenumber = StringField('Phone Number', validators=[DataRequired()])
    location = SelectField('Country', choices=[
        ('KE', 'Kenya'),
        ('TZ', 'Tanzania'),
        ('UG', 'Uganda'),
        ('RW', 'Rwanda')
        ], validators=[DataRequired()])
    gender = SelectField(
        'Gender',
        choices=[('Male'), ('Female'), ('Other')],
        validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired()])
    submit = SubmitField('Signup')

def validate_password(form, field):
    if form.password.data != form.confirm_password.data:
        raise ValidationError('Passwords do not match')

