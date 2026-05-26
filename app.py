from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Configuration
from flask_migrate import Migrate

app = Flask(__name__)

app.config.from_object(Configuration)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

import views
