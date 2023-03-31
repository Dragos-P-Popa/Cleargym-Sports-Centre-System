from app import db
import datetime
from datetime import datetime


# The model of the Booking table
class Sales(db.Model):
    __tablename__ = "sales"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    SaleVal = db.Column(db.Float,  nullable=False)
    Facilityid = db.Column(db.Integer, nullable=False)
    Activityid = db.Column(db.Integer, nullable=False)



