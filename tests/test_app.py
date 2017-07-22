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
        with self.app.session_transaction() as session:
            session.pop('email', None)

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
        # setup a valid user
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
