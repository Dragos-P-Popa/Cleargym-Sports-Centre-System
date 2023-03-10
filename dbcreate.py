from config import SQLALCHEMY_DATABASE_URI
from app import app,db
import os.path

# The method of creating new tables before a first request is made
# was learned from the following thread:
# https://stackoverflow.com/questions/44941757/sqlalchemy-exc-operationalerror-sqlite3-operationalerror-no-such-table
@app.before_first_request
def create_new_tables():
    db.create_all()

