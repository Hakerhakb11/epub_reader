import os
import sys


class Configuration(object):
    if 'ANDROID_PRIVATE' in os.environ:
        BASE_DIR = os.environ.get(
            'ANDROID_PRIVATE', os.path.dirname(os.path.abspath(__file__)))

    elif getattr(sys, 'frozen', False):
        BASE_DIR = os.path.dirname(sys.executable)

    else:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(BASE_DIR, 'library.db')
    SECRET_KEY = os.environ.get(
        'SECRET_KEY', 'cbc101e03f1e485f94e2ea47852dbd55ee7307f0af39ce534a62f202655270b2')
