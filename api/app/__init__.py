from flask import Flask
from flask_pymongo import PyMongo
from config import config
from flask_jwt_extended import JWTManager
from flask_mail import Mail

mongo = PyMongo()
mail = Mail()


def create_app(config_name):
    app = Flask(__name__)
    # Setup the Flask-JWT-Extended extension
    jwt = JWTManager(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    mongo.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    from .resources import resources as resources_blueprint
    app.register_blueprint(resources_blueprint)

    from .respository import repository as respository_blueprint
    app.register_blueprint(respository_blueprint)

    return app
