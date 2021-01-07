import os
import psycopg2

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SHOP_ID = os.environ.get('SECRET_KEY', 5)
    PAY_WAY = os.environ.get('PAY_WAY', 'advcash_rub')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'SecretKey01')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
                                             ('sqlite:///' + os.path.join(basedir, 'app.db')))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    # conn = psycopg2.connect(SQLALCHEMY_DATABASE_URI, sslmode='require')


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
                                             ('sqlite:///' + os.path.join(basedir, 'app_test.db')))
    TESTING = True



    