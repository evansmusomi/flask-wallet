""" Contains application tests mapped to models defined """
import unittest
import datetime
import random
from app.models import User, Expense


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

    def test_get_balance(self):
        """ Tests account balance is returned """
        actual = self.user.get_balance()
        expected = 200
        self.assertEqual(actual, expected)

    def test_add_expense_OK(self):
        """ Tests valid expense is added """
        transaction_date = datetime.datetime(2017, 7, 27)
        expense = Expense(50, 'matatu', transaction_date)
        self.user.add_expense(expense)
        self.assertEqual(len(self.user.expenses), 1)
        self.assertEqual(self.user.expenses[0].amount, 50)
        self.assertEqual(self.user.get_balance(), 150)


class AppTestExpense(unittest.TestCase):
    """ Defines expense tests """

    def setUp(self):
        """ Sets up env for tests """
        transaction_date = datetime.datetime(
            2017, random.randint(1, 7), random.randint(1, 28))
        self.expense = Expense(30, 'matatu', transaction_date)

    def test_expense_OK(self):
        """ Validates expense object """

        self.assertIsNotNone(self.expense)
        self.assertEqual(self.expense.amount, 30)
        self.assertEqual(self.expense.note, 'matatu')
        self.assertIsNotNone(self.expense.transaction_date)

    def test_id_is_generated(self):
        """ Tests id property is generated """
        self.assertIsNotNone(self.expense.id)
