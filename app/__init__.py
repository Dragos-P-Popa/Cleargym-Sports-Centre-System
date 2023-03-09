from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config')
app.app_context().push()
db = SQLAlchemy(app)

migrate = Migrate(app, db)

from app import views, models
