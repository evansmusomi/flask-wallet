""" Contains application tests mapped to routes defined """
import unittest
from run import app


class AppTestCase(unittest.TestCase):
    """ Defines app tests """

    def setUp(self):
        """ Sets up env for tests """
        app.config['TESTING'] = True
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
        """ Tests GET / """
        response = self.app.get('/about')
        self.assertEqual(response.status, "200 OK",
                         "Response status should be 200 OK")
        self.assertIn("Spend or save?".encode(
            'utf-8'), response.data)

    def test_contact_OK(self):
        """ Tests GET / """
        response = self.app.get('/contact')
        self.assertEqual(response.status, "200 OK",
                         "Response status should be 200 OK")
        self.assertIn("Get in touch.".encode(
            'utf-8'), response.data)
