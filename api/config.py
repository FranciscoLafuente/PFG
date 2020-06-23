import os
from mongoengine import connect

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'd4bb6ac5482a68ebf410395f12d26792807e4713'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'localhost')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '1025'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'shodita@shodita.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    # Key to jwt
    JWT_SECRET_KEY = 'irZJcuEKaVfJnrxy43t3HEOsdFc'
    # Dir to bots download and your extension
    UPLOAD_FOLDER = '/app/app/bots/'
    ALLOWED_EXTENSIONS = {'py'}

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_URI = os.environ.get('DEV_DATABASE_URL') or 'mongodb://db:27017/shoditaDB'
    # Connect with mongoengine
    connect('shoditaDB', host='db', port=27017)


class TestingConfig(Config):
    TESTING = True
    MONGO_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite://'


class ProductionConfig(Config):
    MONGO_URI = os.environ.get('DATABASE_URL') or 'mongodb://localhost:9090/shoditaV2'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
