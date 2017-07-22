""" Defines application routes """

from flask import render_template, session, redirect, url_for
from .middleware import create_account, login, logout
from .forms import SignupForm, LoginForm


def page_index():
    """ Renders index page """
    if 'email' in session:
        return redirect(url_for('page_dashboard'))

    signup_form = SignupForm()
    login_form = LoginForm()
    return render_template('index.html', signup_form=signup_form, login_form=login_form)


def page_about():
    """ Renders about page """
    return render_template('about.html')


def page_contact():
    """ Renders contact page """
    return render_template('contact.html')


def page_dashboard():
    """ Renders dashboard page """

    if 'email' not in session:
        return redirect(url_for('page_index'))

    return render_template('dashboard.html', logged_in=True)


def initialize_website_routes(app):
    """ Adds website routes to Flask app """
    if app:
        app.add_url_rule('/', 'page_index', page_index, methods=['GET'])
        app.add_url_rule('/about', 'page_about', page_about, methods=['GET'])
        app.add_url_rule('/contact', 'page_contact',
                         page_contact, methods=['GET'])
        app.add_url_rule('/dashboard', 'page_dashboard',
                         page_dashboard, methods=['GET'])
        app.add_url_rule('/signup', 'create_account',
                         create_account, methods=['POST'])
        app.add_url_rule('/login', 'login', login, methods=['POST'])
        app.add_url_rule('/logout', 'logout', logout, methods=['GET'])
