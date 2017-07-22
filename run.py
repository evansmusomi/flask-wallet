""" Flask Wallet APP definition """

from settings import Config
from app.routes import initialize_website_routes

from flask import Flask

# create Flask app
app = Flask(__name__, template_folder='app/templates',
            static_folder='app/static')
app.config['SECRET_KEY'] = Config.SECRET_KEY

# define routes
initialize_website_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
