""" Routes data requests """

from flask import render_template, redirect, url_for, flash
import i18n

from .forms import SignupForm
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
            flash(i18n.t('wallet.signup_successful',
                         name=form.name.data), "success")

        return redirect(url_for('page_index'))

    flash(i18n.t('wallet.signup_details_invalid'), "error")
    return render_template('index.html', signup_form=form)
