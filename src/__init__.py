from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config

app = Flask(__name__)
app.config.from_object(config.Config)
app.debug = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from src import routes, models
