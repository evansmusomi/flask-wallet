""" Defines form backends """

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Email, Length, NumberRange


class SignupForm(FlaskForm):
    """ Defines the sign up form fields """

    email = StringField('Email', validators=[
        DataRequired('Please enter your email'),
        Email('Please enter your email')])

    password = PasswordField('Password', validators=[
        DataRequired('Please enter your password'),
        Length(min=4, message='Password must be 4 or more characters')])

    name = StringField('Name', validators=[
        DataRequired('Please enter your first name')])

    deposit = DecimalField('Deposit Amount', validators=[
        NumberRange(min=0, message='Please deposit some money')])

    submit = SubmitField('Sign up')
