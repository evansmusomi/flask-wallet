""" Routes data requests """

from flask import render_template, redirect, url_for, flash

from .forms import SignupForm
from .dataservice import DataService

DATA_SERVICE = DataService()


def create_account():
    """ Creates new user account """
    form = SignupForm()

    if form.validate():
        new_user_id = DATA_SERVICE.create_account(
            form.email.data, form.password.data,
            form.name.data, form.deposit.data)

        if new_user_id:
            flash("Sign up successful", "success")

        return redirect(url_for('page_index'))

    flash("Signup details invalid", "error")
    return render_template('index.html', signup_form=form)
