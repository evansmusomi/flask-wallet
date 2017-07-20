""" Defines application routes """

from flask import render_template


def page_index():
    """ Renders index page """
    return render_template('index.html')


def page_about():
    """ Renders about page """
    return render_template('about.html')


def init_website_routes(app):
    """ Adds website routes to Flask app """
    if app:
        app.add_url_rule('/', 'page_index', page_index, methods=['GET'])
        app.add_url_rule('/about', 'page_about', page_about, methods=['GET'])
