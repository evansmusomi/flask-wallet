""" Loads environment configuration """
import os
import dotenv

APP_ROOT = os.path.join(os.path.dirname(__file__), '')
dotenv_path = os.path.join(APP_ROOT, '.env')
dotenv.load(dotenv_path)


class Config(object):
    """ Defines config variables """

    SECRET_KEY = os.environ.get("SECRET_KEY")
