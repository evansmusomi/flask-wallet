""" Defines application routes """

from flask import render_template, session, redirect, url_for
from .middleware import create_account, login, logout, get_account_details
from .middleware import load_user_balance, get_user_expenses, get_user_expense_by_id
from .middleware import add_expense, update_expense, delete_expense
from .forms import SignupForm, LoginForm, AddExpenseForm


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

    account_balance = load_user_balance()
    user_expenses = get_user_expenses()
    add_expense_form = AddExpenseForm()
    return render_template('dashboard.html', logged_in=True, balance=account_balance, expense_form=add_expense_form, expenses=user_expenses)


def page_edit_expense(expense_id):
    """ Renders edit expense page """

    if 'email' not in session:
        return redirect(url_for('page_index'))

    user_expense = get_user_expense_by_id(expense_id)
    return render_template('edit_expense.html', logged_in=True, expense_form=AddExpenseForm(obj=user_expense), expense_id=expense_id)


def page_profile():
    """ Renders user account page """

    if 'email' not in session:
        return redirect(url_for('page_index'))

    account_details = get_account_details()
    return render_template('profile.html', logged_in=True, account=account_details)


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
        app.add_url_rule('/expenses', 'add_expense',
                         add_expense, methods=['POST'])
        app.add_url_rule('/expenses/<string:expense_id>', 'page_edit_expense',
                         page_edit_expense, methods=['GET'])
        app.add_url_rule('/expenses/<string:expense_id>', 'update_expense',
                         update_expense, methods=['POST'])
        app.add_url_rule('/expenses/<string:expense_id>/delete',
                         'delete_expense', delete_expense, methods=['GET'])
        app.add_url_rule('/profile',
                         'page_profile', page_profile, methods=['GET'])
