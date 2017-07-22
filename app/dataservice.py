""" Defines data layer wrapper """
from .models import User


class DataService:
    """ Provides data to the rest of the app """

    def __init__(self):
        self.USERS = {}

    def create_account(self, email, password, name, deposit):
        """ Adds user to data store """
        new_user = User(email, password, name, deposit)
        self.USERS[email] = new_user
        return str(new_user.id)
