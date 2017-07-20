""" Flask Wallet APP definition """

from settings import Config
from routes import init_website_routes

from flask import Flask

# create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY

# define routes
init_website_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
