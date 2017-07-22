""" Model definitions """
import uuid
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
        self.balance = deposit

    def check_password(self, password):
        """ Compares password hash with password """
        return check_password_hash(self.password_hash, password)

    @property
    def id(self):
        """ Returns user id property """
        return self.__id
