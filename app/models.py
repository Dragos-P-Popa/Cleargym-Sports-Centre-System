from app import db
import datetime
from datetime import datetime


# The model of the Booking table
class Sales(db.Model):
    __tablename__ = "sales"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    saleValue = db.Column(db.Float,  nullable=False)
    facilityId = db.Column(db.Integer, nullable=False)
    activityId = db.Column(db.Integer, nullable=False)
    saleDate = db.Column(db.Date, default=datetime.now())



