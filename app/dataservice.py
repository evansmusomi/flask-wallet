""" Defines data layer wrapper """
import datetime
import i18n
from .models import User, Expense

# Add locales folder to translation path
i18n.load_path.append('app/locales')


class DataService:
    """ Provides data to the rest of the app """
    USERS = {}

    def __init__(self):
        """ Initializes data service """
        pass

    def create_account(self, email, password, name, deposit):
        """ Adds user to data store """
        if email not in self.USERS:
            new_user = User(email, password, name, deposit)
            self.USERS[email] = new_user
            return str(new_user.id)
        else:
            return str(self.USERS[email].id)

    def login(self, email, password):
        """ Authenticates user """
        if email in self.USERS:
            user = self.USERS[email]
            if user.check_password(password):
                return user

        return None

    def load_user_balance(self, email):
        """ Gets user account balance """
        if email in self.USERS:
            return self.USERS[email].get_balance()

        return i18n.t('wallet.wallet_not_found')

    def add_expense(self, email, amount, note):
        """ Adds expense to user account """
        if email in self.USERS:
            transaction_date = datetime.date.today().strftime('%Y/%m/%d')
            expense = Expense(amount, note, transaction_date)
            self.USERS[email].add_expense(expense)
            return i18n.t('wallet.expense_added')

        return i18n.t('wallet.wallet_not_found')

    def get_user_expenses(self, email):
        """ Gets user's expenses """
        if email in self.USERS:
            return self.USERS[email].expenses

        return i18n.t('wallet.wallet_not_found')

    def get_user_expense_by_id(self, expense_id, email):
        """ Gets user expense by id """
        if email in self.USERS:
            for expense in self.USERS[email].expenses:
                if expense_id == str(expense.id):
                    return expense

            return i18n.t('wallet.expense_not_found')

        return i18n.t('wallet.wallet_not_found')
