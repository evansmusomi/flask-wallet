""" Contains application tests mapped to models defined """
import unittest
from app.models import User


class AppTestUser(unittest.TestCase):
    """ Defines user tests """

    def setUp(self):
        """ Sets up env for tests """
        self.user = User('user@mail.com', 'secret', 'John', 200)

    def test_id_is_generated(self):
        """ Tests id property is generated """
        self.assertIsNotNone(self.user.id)

    def test_password_is_hashed(self):
        """ Tests plain password isn't stored """
        self.assertNotEqual(self.user.password_hash, 'secret')
