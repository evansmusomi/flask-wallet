""" Defines data layer wrapper """
from .models import User


class DataService:
    """ Provides data to the rest of the app """

    def __init__(self):
        """ Initializes data service """
        self.USERS = {}

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

        return False
