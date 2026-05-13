import os

class Configuration(object):
    basedir = os.path.abspath(os.path.dirname(__name__)) 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'library.db')

