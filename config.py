import os
import sys


class Configuration(object):
    if getattr(sys, 'frozen', False):
        BASE_DIR = os.path.dirname(sys.executable)
    else:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'library.db')
    SECRET_KEY = 'cbc101e03f1e485f94e2ea47852dbd55ee7307f0af39ce534a62f202655270b2'

# Command to create a single executable file using PyInstaller with the specified options and additional data files.

# poetry run pyinstaller --noconfirm --onefile --windowed --add-data "templates;templates" --add-data "static;static" --add-data "home/templates;home/templates" --add-data "books/templates;books/templates" main.py