from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.from_object('config')
app.app_context().push()
CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
#app.config['SECRET_KEY'] = "our0secret0key"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'cleargymstaff@gmail.com'
app.config['MAIL_PASSWORD'] = 'yhnhrwgsapafwdin'
mail = Mail(app)

from app import views, models
