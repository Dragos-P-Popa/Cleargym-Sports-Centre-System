from app import db
import datetime
from datetime import datetime


# The model of the Booking table
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    userId = db.Column(db.String(50), nullable=False)
    facilityId = db.Column(db.Integer, nullable=False)
    activityId = db.Column(db.Integer, nullable=False)
    createDate = db.Column(db.Date, nullable=False, default=datetime.now())
    bookingDate = db.Column(db.Date, nullable=False)
    bookingTime = db.Column(db.Time, nullable=False)
    bookingLength = db.Column(db.Time, nullable=False)
    bookingEndTime = db.Column(db.Time, nullable=False)
    bookingType = db.Column(db.String(100), nullable=False)
