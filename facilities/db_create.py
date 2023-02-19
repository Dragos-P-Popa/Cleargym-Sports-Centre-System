from config import SQLALCHEMY_DATABASE_URI
from facilities import db
import os.path

db.create_all()
