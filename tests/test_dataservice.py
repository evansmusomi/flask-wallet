""" Contains application tests mapped to data service """
import unittest
from app.dataservice import DataService


class AppTestDataService(unittest.TestCase):
    """ Defines data service tests """

    def setUp(self):
        """ Sets up env for tests """
        self.dataservice = DataService()

    def test_user_account_created(self):
        """ Tests user account is created successfully """
        self.dataservice.create_account(
            'user@mail.com', 'secret', 'John', 200)
        self.assertEqual(self.dataservice.USERS['user@mail.com'].name, "John")

    def test_duplicate_user_account_not_created(self):
        """ Tests user doesn't create duplicate accounts """
        self.dataservice.create_account(
            'user@mail.com', 'secret', 'John', 200)
        self.dataservice.create_account(
            'user@mail.com', 'secret', 'John', 200)

        self.assertEqual(len(self.dataservice.USERS), 1)
