import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    # MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    # MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
    #    ['true', 'on', '1']
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SERVER = "localhost"
    MAIL_PORT = "1025"
    MAIL_USERNAME = "shodita@shodita.com"
    MAIL_PASSWORD = ""
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_URI = os.environ.get('DEV_DATABASE_URL') or \
        'mongodb://localhost:27017/shodita'


class TestingConfig(Config):
    TESTING = True
    MONGO_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'


class ProductionConfig(Config):
    MONGO_URI = os.environ.get('DATABASE_URL') or \
        'mongodb://localhost:27017/shodita/mongodb_test'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
