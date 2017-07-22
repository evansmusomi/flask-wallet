""" Model definitions """
import uuid
from werkzeug import generate_password_hash, check_password_hash


class User:
    """ Defines user blueprint """
    __id = None

    def __init__(self, email, password, name, deposit):
        """ Initializes user object """
        self.__id = uuid.uuid4()
        self.email = email.lower()
        self.password_hash = self.set_password(password)
        self.name = name.title()
        self.balance = deposit

    def set_password(self, password):
        """ Generates password hash from password """
        self.password_hash = generate_password_hash(password)

    @property
    def id(self):
        """ Returns user id property """
        return self.__id
