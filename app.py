from flask import Flask

from books.views import books
from config import Configuration
from home.views import home
from models import db

app = Flask(__name__)

app.config.from_object(Configuration)
db.init_app(app)

app.register_blueprint(home)
app.register_blueprint(books)
