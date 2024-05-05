#!/usr/bin/env python3
""" Module to define the forms used in the app. """

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField
from wtforms import SubmitField, ValidationError
from wtforms.validators import DataRequired, Email
from app.models import User


class LoginForm(FlaskForm):
    """
    Represents the login form.

    Attributes:
        username (StringField): Field for entering the username.
        password (PasswordField): Field for entering the password.
        submit (SubmitField): Button for submitting the form.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    # username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password')
    submit = SubmitField('Login')

    def get_username(self):
        """
        Getter method for the username field.

        Returns:
            str: The value entered in the username field.
        """
        return self.username.data

    def get_password(self):
        """
        Getter method for the password field.

        Returns:
            str: The value entered in the password field.
        """
        return self.password.data


class SignupForm(FlaskForm):
    """
    Represents the signup form.

    Attributes:
        firstname (StringField): Field for entering the first name.
        lastname (StringField): Field for entering the last name.
        username (StringField): Field for entering the username.
        phonenumber (StringField): Field for entering the phone number.
        location (SelectField): Field for selecting the country.
        gender (SelectField): Field for selecting the gender.
        password (PasswordField): Field for entering the password.
        confirm_password (PasswordField): Field for confirming the password.
        submit (SubmitField): Button for submitting the form.
    """
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
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired()])
    submit = SubmitField('Signup')

    def email_exists(form, field):
        """
        Checks if the email already exists in the User table.

        Args:
            form (SignupForm): The signup form object.
            field (StringField): The email field.

        Returns:
            bool: True if the email exists, False otherwise.
        """
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already exists')

    email = StringField('Email', validators=[DataRequired(), Email(), email_exists])

    def validate_password(form, field):
        """ Check if the password and confirm password fields match. """
        if form.password.data != form.confirm_password.data:
            raise ValidationError('Passwords do not match')
