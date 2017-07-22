""" Contains application tests mapped to data service """
import unittest
from app.dataservice import DataService


class AppTestDataService(unittest.TestCase):
    """ Defines data service tests """

    def setUp(self):
        """ Sets up env for tests """
        self.dataservice = DataService()
        self.dataservice.create_account(
            'john@doe.com', 'secret', 'John', 500)
        self.user = self.dataservice.USERS['john@doe.com']

    def test_user_account_created(self):
        """ Tests user account is created successfully """
        self.dataservice.create_account(
            'user@mail.com', 'secret', 'User', 200)

        actual = self.dataservice.USERS['user@mail.com'].name
        expected = "User"

        self.assertEqual(actual, expected)

    def test_duplicate_user_account_not_created(self):
        """ Tests user doesn't create duplicate accounts """
        self.dataservice.create_account(
            'john@doe.com', 'secret', 'John', 500)

        actual = len(self.dataservice.USERS)
        expected = 1
        self.assertEqual(actual, expected)

    def test_login_with_valid_credentials(self):
        """ Tests valid user logs in successfully """
        actual = self.dataservice.login('john@doe.com', 'secret')
        expected = self.user
        self.assertEqual(actual, expected)

    def test_login_with_wrong_credentials(self):
        """ Tests invalid user doesn't log in successfully """
        actual = self.dataservice.login('john@doe.com', 'wrong-password')
        expected = False
        self.assertEqual(actual, expected)
