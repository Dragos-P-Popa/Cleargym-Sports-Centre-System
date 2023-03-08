from app import db
from datetime import datetime


# Creating the columns
class Booking(db.Model):
    __tablename__ = "booking_table"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    userId = db.Column(db.String(500), nullable=False)
    facilitiesId = db.Column(db.Integer, nullable = False)
    activityId = db.Column(db.Integer,
                           db.ForeignKey('activity_table.activityId'),
                           nullable=False)
    createDate = db.Column(db.Date, nullable=False)
    bookingDate = db.Column(db.Date, nullable=False)
    bookingTime = db.Column(db.Time, nullable=False)
    bookingLength = db.Column(db.Time, nullable=False)
    bookingEndTime = db.Column(db.Time, nullable=False)
    bookingType = db.Column(db.String(500), nullable=False)
    teamEvent = db.Column(db.Boolean, nullable=False)
    activity = db.relationship("Activity",
                               back_populates="booking")


class Activity(db.Model):
    __tablename__ = "activity_table"
    activityId = db.Column(db.Integer, primary_key=True, nullable=False)
    activityType = db.Column(db.String(100), nullable=False)
    activityStartTime = db.Column(db.Time, nullable=False)
    activityEndTime = db.Column(db.Time, nullable=False)
    activityDay = db.Column(db.String(10), nullable=False)
    booking = db.relationship("Booking",
                              back_populates="activity")

    # The one-to-many relationship set up is explained in more detail in the
    # following SQLAlchemy documentation:
    # https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#many-to-one
    # (It is one activity to many bookings)
