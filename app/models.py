""" Model definitions """
import uuid
import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User:
    """ Defines user blueprint """
    __id = None

    def __init__(self, email, password, name, deposit):
        """ Initializes user object """
        self.__id = uuid.uuid4()
        self.email = email.lower()
        self.password_hash = generate_password_hash(password)
        self.name = name.title()
        self.__balance = deposit
        self.expenses = []

    def check_password(self, password):
        """ Compares password hash with password """
        return check_password_hash(self.password_hash, password)

    def get_balance(self):
        """ Returns account balance """
        return self.__balance

    def add_expense(self, expense):
        """ Adds expense to user wallet """
        self.expenses.append(expense)
        self.__balance -= expense.amount

    def delete_expense(self, expense):
        """ Deletes an expense from user's wallet """
        expense_amount = expense.amount
        self.expenses.remove(expense)
        self.__balance += expense_amount

    @property
    def id(self):
        """ Returns user id property """
        return self.__id


class Expense:
    """ Defines Expense Blueprint """
    __id = None

    def __init__(self, amount, note, transaction_date):
        """ Initializes expense object """
        self.__id = uuid.uuid4().hex[:10].upper()
        self.amount = amount
        self.note = note
        self.transaction_date = transaction_date

    @property
    def id(self):
        """ Returns expense id property """
        return self.__id

    def update(self, amount, note):
        """ Updates expense attributes """
        self.amount = amount
        self.note = note
        self.transaction_date = datetime.date.today().strftime('%Y/%m/%d')
