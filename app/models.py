from app import db
from datetime import datetime
class booking(db.Model):
    id = db.Column(db.Integer, primary_key=True ,nullable=False)
    userId = db.Column(db.String(500),nullable=False)
    createDate = db.Column(db.Date,nullable=False)
    bookingDate = db.Column(db.Date,nullable=False)
    bookingTime = db.Column(db.Time , default=datetime.utcnow(),nullable=False)
    bookingLength = db.Column(db.Time , default=datetime.utcnow(),nullable=False)
    bookingType = db.Column(db.String(500),nullable=False)
    teamEvent= db.Column(db.Boolean,nullable=False)