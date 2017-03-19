import os
basedir = os.path.abspath(os.path.dirname(__file__))


DATABASE = 'site.db'
DEBUG = True
DATABASE_PATH = os.path.join(basedir, DATABASE)
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "this is some kind of secret"
