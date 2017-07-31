""" Contains application tests mapped to models defined """
import unittest
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
        expense = Expense(50, 'matatu')
        self.user.add_expense(expense)
        self.assertEqual(len(self.user.expenses), 1)
        self.assertEqual(self.user.expenses[0].amount, 50)
        self.assertEqual(self.user.get_balance(), 150)

    def test_add_expense_INVALID(self):
        """ Tests adding an invalid expense """
        expense = "invalid expense"
        actual = self.user.add_expense(expense)
        expected = False
        self.assertEqual(actual, expected)

    def test_delete_expense_OK(self):
        """ Tests expense is deleted correctly """
        expense = Expense(50, 'taxi')
        self.user.add_expense(expense)
        self.assertTrue(self.user.delete_expense(expense))
        self.assertEqual(len(self.user.expenses), 0)

    def test_delete_expense_INVALID(self):
        """ Tests failure deleting an expense """
        expense = "invalid expense"
        actual = self.user.delete_expense(expense)
        expected = False
        self.assertEqual(actual, expected)

    def test_topup_OK(self):
        """ Tests top up works ok """
        initial_balance = self.user.get_balance()
        self.user.topup(500)

        expected = initial_balance + 500
        actual = self.user.get_balance()
        self.assertEqual(actual, expected)


class AppTestExpense(unittest.TestCase):
    """ Defines expense tests """

    def setUp(self):
        """ Sets up env for tests """
        self.expense = Expense(30, 'matatu')

    def test_expense_OK(self):
        """ Validates expense object """

        self.assertIsNotNone(self.expense)
        self.assertEqual(self.expense.amount, 30)
        self.assertEqual(self.expense.note, 'matatu')
        self.assertIsNotNone(self.expense.transaction_date)

    def test_id_is_generated(self):
        """ Tests id property is generated """
        self.assertIsNotNone(self.expense.id)
