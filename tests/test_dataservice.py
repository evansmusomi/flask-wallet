""" Contains application tests mapped to data service """
import unittest
import datetime
import i18n
from app.dataservice import DataService

# Add locales folder to translation path
i18n.load_path.append('app/locales')


class AppTestDataService(unittest.TestCase):
    """ Defines data service tests """

    def setUp(self):
        """ Sets up env for tests """
        self.dataservice = DataService()
        self.dataservice.create_account(
            'john@doe.com', 'secret', 'John', 500)
        self.user = self.dataservice.USERS['john@doe.com']

    def tearDown(self):
        """ Clears env for tests """
        self.dataservice = None
        self.user = None

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
        expected = None
        self.assertEqual(actual, expected)

    def test_load_user_balance_OK(self):
        """ Tests user balance is loaded OK for valid user """
        actual = self.dataservice.load_user_balance('john@doe.com')
        expected = self.user.get_balance()
        self.assertEqual(actual, expected)

    def test_load_user_balance_INVALID(self):
        """ Tests None is returned when balance is queried for invalid user """
        actual = self.dataservice.load_user_balance('invalid@user.com')
        expected = i18n.t('wallet.wallet_not_found')
        self.assertEqual(actual, expected)

    def test_add_expense_OK(self):
        """ Tests adding expenses works fine """
        initial_balance = self.dataservice.load_user_balance('john@doe.com')
        self.dataservice.add_expense('john@doe.com', 50, 'matatu')
        expected = initial_balance - 50
        actual = self.dataservice.load_user_balance('john@doe.com')
        self.assertEqual(actual, expected)

    def test_add_expense_INVALID_USER(self):
        """ Tests adding expenses to invalid user accounts """
        actual = self.dataservice.add_expense('invalid@user.com', 50, 'matatu')
        expected = i18n.t('wallet.wallet_not_found')
        self.assertEqual(actual, expected)

    def test_get_user_expenses_OK(self):
        """ Tests user expenses are loaded OK for valid user """
        actual = self.dataservice.get_user_expenses('john@doe.com')
        expected = self.user.expenses
        self.assertEqual(actual, expected)

    def test_get_user_expenses_INVALID(self):
        """ Tests getting expenses from invalid user account """
        actual = self.dataservice.get_user_expenses('invalid@user.com')
        expected = i18n.t('wallet.wallet_not_found')
        self.assertEqual(actual, expected)
