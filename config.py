import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'nifdl>jfdf@md!'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')or \
    'sqlite:///shop.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False



