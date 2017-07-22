""" Defines application routes """

from flask import render_template
from .middleware import create_account
from .forms import SignupForm


def page_index():
    """ Renders index page """
    signup_form = SignupForm()
    return render_template('index.html', signup_form=signup_form)


def page_about():
    """ Renders about page """
    return render_template('about.html')


def page_contact():
    """ Renders contact page """
    return render_template('contact.html')


def page_dashboard():
    """ Renders dashboard page """
    return render_template('dashboard.html')


def initialize_website_routes(app):
    """ Adds website routes to Flask app """
    if app:
        app.add_url_rule('/', 'page_index', page_index,
                         methods=['GET'])
        app.add_url_rule('/about', 'page_about', page_about, methods=['GET'])
        app.add_url_rule('/contact', 'page_contact',
                         page_contact, methods=['GET'])
        app.add_url_rule('/dashboard', 'page_dashboard',
                         page_dashboard, methods=['GET'])
        app.add_url_rule('/signup', 'create_account',
                         create_account, methods=['POST'])
