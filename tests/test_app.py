""" Contains application tests mapped to routes defined """
import unittest
import html
import i18n
from run import app
from app.dataservice import DataService

# Add locales folder to translation path
i18n.load_path.append('app/locales')


class AppTestCase(unittest.TestCase):
    """ Defines app tests """

    def setUp(self):
        """ Sets up env for tests """
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SECRET_KEY'] = 'secret-key'
        self.app = app.test_client()

        self.dataservice = DataService()

        with self.app.session_transaction() as session:
            session.pop('email', None)

    def tearDown(self):
        """ Tears down after tests """
        self.dataservice.USERS = None

    def test_index_OK_VISITOR(self):
        """ Tests GET / when not logged in """
        response = self.app.get('/')
        self.assertEqual(response.status, "200 OK",
                         "Response status should be 200 OK")
        self.assertIn("Make better spending decisions.".encode(
            'utf-8'), response.data)

    def test_index_OK_USER(self):
        """ Tests GET / when logged in """
        with self.app.session_transaction() as session:
            session['email'] = 'john@doe.com'

        response = self.app.get('/')
        self.assertEqual(response.status, "302 FOUND")

    def test_about_OK(self):
        """ Tests GET /about """
        response = self.app.get('/about')
        self.assertEqual(response.status, "200 OK",
                         "Response status should be 200 OK")
        self.assertIn("Spend or save?".encode(
            'utf-8'), response.data)

    def test_contact_OK(self):
        """ Tests GET /contact """
        response = self.app.get('/contact')
        self.assertEqual(response.status, "200 OK",
                         "Response status should be 200 OK")
        self.assertIn("Get in touch.".encode(
            'utf-8'), response.data)

    def test_create_account_OK(self):
        """ Tests sign up with valid details """
        new_user_info = dict(
            email="john@doe.com",
            password="secret",
            name="John",
            deposit=500
        )

        response = self.app.post(
            '/signup', data=new_user_info, follow_redirects=True)

        self.assertEqual(response.status, "200 OK")
        self.assertIn(i18n.t('wallet.signup_successful', name="John"),
                      html.unescape(response.data.decode("utf-8")))

    def test_create_account_INVALID(self):
        """ Tests sign up with invalid details """
        new_user_info = dict(
            email="name@mail",
            password="secret"
        )

        response = self.app.post(
            '/signup', data=new_user_info)

        self.assertEqual(response.status, "200 OK")
        self.assertIn(i18n.t('wallet.signup_invalid'),
                      html.unescape(response.data.decode("utf-8")))

    def test_dashboard_OK_VISITOR(self):
        """ Tests GET /dashboard when not logged in """
        response = self.app.get('/dashboard')
        self.assertEqual(response.status, "302 FOUND",
                         "Response status should be 302 FOUND")

    def test_dashboard_OK_USER(self):
        """ Tests GET /dashboard when logged in """
        with self.app.session_transaction() as session:
            session['email'] = 'john@doe.com'

        response = self.app.get('/dashboard')
        self.assertEqual(response.status, "200 OK",
                         "Response status should be 200 OK")
        self.assertIn("Left to spend!".encode(
            'utf-8'), response.data)

    def test_log_in_OK(self):
        """ Tests log in with valid details """
        self.dataservice.create_account('john@doe.com', 'secret', 'John', 500)

        user_info = dict(
            email="john@doe.com",
            password="secret"
        )

        response = self.app.post(
            '/login', data=user_info, follow_redirects=True)

        self.assertEqual(response.status, "200 OK")
        self.assertIn(i18n.t('wallet.login_successful', name="John"),
                      html.unescape(response.data.decode("utf-8")))

    def test_log_in_FAILED(self):
        """ Tests log in with wrong details """
        user_info = dict(email="john@doe.com", password="wrong-password")

        response = self.app.post('/login', data=user_info)

        self.assertEqual(response.status, "200 OK")
        self.assertIn(i18n.t('wallet.login_failed'),
                      html.unescape(response.data.decode("utf-8")))

    def test_log_in_INVALID(self):
        """ Tests log in with invalid details """
        user_info = dict(email="name@mail")

        response = self.app.post('/login', data=user_info)

        self.assertEqual(response.status, "200 OK")
        self.assertIn(i18n.t('wallet.login_invalid'),
                      html.unescape(response.data.decode("utf-8")))

    def test_log_out_OK(self):
        """ Tests log out works for logged in users """
        with self.app.session_transaction() as session:
            session['email'] = 'john@doe.com'

        response = self.app.get('/logout', follow_redirects=True)

        self.assertEqual(response.status, "200 OK")
        self.assertIn(i18n.t('wallet.logged_out'),
                      html.unescape(response.data.decode("utf-8")))

    def test_add_expense_LOGGED_OUT(self):
        """ Tests add expense by logged out user """
        expense_info = dict(
            amount=40,
            note="matatu"
        )

        response = self.app.post(
            '/expenses', data=expense_info)

        self.assertEqual(response.status, "302 FOUND")

    def test_add_expense_OK(self):
        """ Tests add expense with valid inputs """
        self.create_account_and_session()

        expense_info = dict(
            amount=40,
            note="matatu"
        )

        response = self.app.post(
            '/expenses', data=expense_info, follow_redirects=True)

        self.assertEqual(response.status, "200 OK")
        self.assertIn(i18n.t('wallet.expense_added'),
                      html.unescape(response.data.decode("utf-8")))

    def test_add_expense_INVALID(self):
        """ Tests add expense with invalid inputs """
        self.create_account_and_session()

        expense_info = dict(
            note="matatu"
        )

        response = self.app.post(
            '/expenses', data=expense_info, follow_redirects=True)

        self.assertEqual(response.status, "200 OK")
        self.assertIn(i18n.t('wallet.expense_invalid'),
                      html.unescape(response.data.decode("utf-8")))

    def create_account_and_session(self, logged_in=True):
        """ Creates an account and session """
        self.dataservice.create_account('john@doe.com', 'secret', 'John', 500)

        if logged_in:
            with self.app.session_transaction() as session:
                session['email'] = 'john@doe.com'

    def create_expense(self):
        """ Creates example expense by John Doe """
        self.dataservice.add_expense('john@doe.com', 200, 'shopping')
        return self.dataservice.USERS['john@doe.com'].expenses[0]

    def test_edit_expense_OK(self):
        """ Tests editing an expense GET /expenses/<expense_id> """
        self.create_account_and_session()
        expense = self.create_expense()

        response = self.app.get("/expenses/{}".format(expense.id))
        self.assertEqual(response.status, "200 OK",
                         "Response status should be 200 OK")
        self.assertIn("Edit Expense".encode(
            'utf-8'), response.data)
        self.assertIn(str(expense.amount).encode('utf-8'), response.data)
        self.assertIn(str(expense.note).encode('utf-8'), response.data)

    def test_edit_expense_LOGGED_OUT(self):
        """ Tests editing an expense while not logged in """

        expense = self.create_expense()

        response = self.app.get("/expenses/{}".format(expense.id))
        self.assertEqual(response.status, "302 FOUND")

    def test_update_expense_LOGGED_OUT(self):
        """ Tests update expense by logged out user """
        expense = self.create_expense()

        expense_info = dict(
            amount=100,
            note="matatu"
        )

        response = self.app.post(
            "/expenses/{}".format(expense.id), data=expense_info)

        self.assertEqual(response.status, "302 FOUND")

    def test_update_expense_OK(self):
        """ Tests add expense with valid inputs """
        self.create_account_and_session()

        expense = self.create_expense()

        expense_info = dict(
            amount=100,
            note="matatu"
        )

        response = self.app.post(
            "/expenses/{}".format(expense.id), data=expense_info, follow_redirects=True)

        self.assertEqual(response.status, "200 OK")
        self.assertIn(i18n.t('wallet.expense_updated'),
                      html.unescape(response.data.decode("utf-8")))

    def test_update_expense_INVALID(self):
        """ Tests add expense with invalid inputs """
        self.create_account_and_session()

        expense = self.create_expense()

        expense_info = dict(
            amount=100
        )

        response = self.app.post(
            "/expenses/{}".format(expense.id), data=expense_info)

        self.assertEqual(response.status, "200 OK")
        self.assertIn(i18n.t('wallet.expense_invalid'),
                      html.unescape(response.data.decode("utf-8")))

    def test_delete_expense_OK(self):
        """ Tests deleting expense works """
        self.create_account_and_session()

        expense = self.create_expense()

        response = self.app.get(
            "/expenses/{}/delete".format(expense.id), follow_redirects=True)

        self.assertEqual(response.status, "200 OK")
        self.assertIn(i18n.t('wallet.expense_deleted'),
                      html.unescape(response.data.decode("utf-8")))

    def test_delete_expense_LOGGED_OUT(self):
        """ Tests deleting expense when logged out """
        expense = self.create_expense()

        response = self.app.get(
            "/expenses/{}/delete".format(expense.id))

        self.assertEqual(response.status, "302 FOUND")

    def test_profile_restricted_VISITOR(self):
        """ Tests GET /profile when not logged in """
        response = self.app.get('/profile')
        self.assertEqual(response.status, "302 FOUND",
                         "Response status should be 302 FOUND")

    def test_profile_OK_USER(self):
        """ Tests GET /profile when logged in """
        self.create_account_and_session()
        user = self.dataservice.USERS['john@doe.com']

        response = self.app.get('/profile')
        self.assertEqual(response.status, "200 OK",
                         "Response status should be 200 OK")
        self.assertIn(i18n.t("wallet.profile_details").encode(
            'utf-8'), response.data)
