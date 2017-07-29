""" Routes data requests """

from flask import render_template, redirect, url_for, flash, session
import i18n

from .forms import SignupForm, LoginForm, AddExpenseForm
from .dataservice import DataService

# Add locales folder to translation path
i18n.load_path.append('app/locales')

# Initialize Data Service
DATA_SERVICE = DataService()


def create_account():
    """ Creates new user account from signup form data """

    form = SignupForm()

    if form.validate():
        new_user_id = DATA_SERVICE.create_account(
            form.email.data, form.password.data,
            form.name.data, form.deposit.data)

        if new_user_id:
            # Create new session and redirect to dashboard
            flash(i18n.t('wallet.signup_successful',
                         name=form.name.data), "success")
            session['email'] = form.email.data
            return redirect(url_for('page_dashboard'))

    flash(i18n.t('wallet.signup_invalid'), "error")
    return render_template('index.html', signup_form=form, login_form=LoginForm())


def login():
    """ Authenticates users based on login form data """

    form = LoginForm()

    if form.validate():
        authenticated_user = DATA_SERVICE.login(
            form.email.data, form.password.data)

        if authenticated_user:
            # Create new session and redirect to dashboard
            flash(i18n.t('wallet.login_successful',
                         name=authenticated_user.name), "success")
            session['email'] = form.email.data
            return redirect(url_for('page_dashboard'))

        flash(i18n.t('wallet.login_failed'), "error")
        return render_template('index.html', login_form=form, signup_form=SignupForm())

    flash(i18n.t('wallet.login_invalid'), "error")
    return render_template('index.html', login_form=form, signup_form=SignupForm())


def logout():
    """ Clears user session and redirects to index page """
    session.pop('email', None)
    flash(i18n.t('wallet.logged_out'), "success")
    return redirect(url_for('page_index'))


def load_user_balance():
    """ Gets user account balance """
    account_balance = DATA_SERVICE.load_user_balance(session['email'])
    return account_balance


def add_expense():
    """ Adds expense to logged in users wallet """
    if 'email' not in session:
        return redirect(url_for('page_index'))

    form = AddExpenseForm()
    if form.validate():
        status = DATA_SERVICE.add_expense(
            session['email'], form.amount.data, form.note.data)

        flash(status, "success")
        return redirect(url_for('page_dashboard'))

    flash(i18n.t('wallet.expense_invalid'), "error")
    add_expense_form = AddExpenseForm()
    user_expenses = get_user_expenses()
    return render_template('dashboard.html', logged_in=True, balance=load_user_balance(), expense_form=add_expense_form, expenses=user_expenses)


def get_user_expenses():
    """ Gets user expenses """
    account_expenses = DATA_SERVICE.get_user_expenses(session['email'])
    return account_expenses
