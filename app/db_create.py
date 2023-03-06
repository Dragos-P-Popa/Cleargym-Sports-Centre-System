from config import SQLALCHEMY_DATABASE_URI
from app import db
import os.path

#commit the changes to the databse
db.session.commit()

db.create_all()
