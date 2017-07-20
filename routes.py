""" Defines application routes """

from flask import render_template


def page_index():
    """ Renders index page """
    return render_template('index.html', selected_menu_item='index')


def init_website_routes(app):
    """ Adds website routes to Flask app """
    if app:
        app.add_url_rule('/', 'page_index', page_index, methods=['GET'])
