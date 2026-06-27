import os


class Configuration(object):
    basedir = os.path.abspath(os.path.dirname(__name__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(basedir, 'library.db')
    SECRET_KEY = "cbc101e03f1e485f94e2ea47852dbd55ee7307f0af39ce534a62f202655270b2"
