""" Contains application tests mapped to routes defined """
import unittest
from run import app


class AppTestCase(unittest.TestCase):
    """ Defines app tests """

    def setUp(self):
        """ Sets up env for tests """
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()

    def tearDown(self):
        """ Tears down after tests """
        pass

    def test_index_OK(self):
        """ Tests GET / """
        response = self.app.get('/')
        self.assertEqual(response.status, "200 OK",
                         "Response status should be 200 OK")
        self.assertIn("Make better spending decisions.".encode(
            'utf-8'), response.data)

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
            email="name@mail.com",
            password="12345",
            name="Name",
            deposit=200
        )

        response = self.app.post(
            '/signup', data=new_user_info, follow_redirects=True)

        self.assertEqual(response.status, "200 OK")
        self.assertIn("Sign up successful".encode('utf-8'), response.data)

    def test_create_account_INVALID(self):
        """ Tests sign up with invalid details """
        new_user_info = dict(
            email="name@mail",
            password="secret"
        )

        response = self.app.post(
            '/signup', data=new_user_info)

        self.assertEqual(response.status, "200 OK")
        self.assertIn("Signup details invalid".encode('utf-8'), response.data)

    def test_dashboard_OK(self):
        """ Tests GET /dashboard """
        response = self.app.get('/dashboard')
        self.assertEqual(response.status, "200 OK",
                         "Response status should be 200 OK")
        self.assertIn("Left to spend!".encode(
            'utf-8'), response.data)
