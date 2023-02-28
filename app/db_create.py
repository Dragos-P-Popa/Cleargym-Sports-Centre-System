from config import SQLALCHEMY_DATABASE_URI
from app import db
import os.path

# delete all data from the Facility table
db.session.query(Facility).delete()

# commit the changes to the database
db.session.commit()

db.create_all()
