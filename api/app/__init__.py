from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from config import config
from flask_jwt_extended import JWTManager
from flask_mail import Mail

mongo = PyMongo()
login_manager = LoginManager()
login_manager.login_view = 'login'
mail = Mail()
UPLOAD_FOLDER = '/app/app/bots/'
ALLOWED_EXTENSIONS = {'py'}


def create_app(config_name):
    app = Flask(__name__)
    # Setup the Flask-JWT-Extended extension
    app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
    jwt = JWTManager(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    mongo.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    from .resources import resources as resources_blueprint
    app.register_blueprint(resources_blueprint)

    from .respository import repository as respository_blueprint
    app.register_blueprint(respository_blueprint)

    return app
