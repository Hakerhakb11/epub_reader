from flask import Flask
from flask_migrate import Migrate

from books.blueprint import books
from config import Configuration
from models import db

app = Flask(__name__)

import views  # noqa: E402, F401

app.config.from_object(Configuration)
db.init_app(app)
migrate = Migrate(app, db)


app.register_blueprint(books)

