from app import db

# the Facilities class represents facilities in the Sports Centre
class Facility(db.Model):
    # id attribute is a primary key for Facility model
    id = db.Column(db.Integer, primary_key=True)
    # the following attributes can not be left empty, therefore nullable=False
    facilityName = db.Column(db.String(500), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    openingTime = db.Column(db.Time, nullable=False)
    closingTime = db.Column(db.Time, nullable=False)
    managerId = db.Column(db.Integer, nullable=False)


def __init__(self, facilityName, capacity, openingTime, closingTime, managerId):
    self.facilityName = facilityName
    self.capacity = capacity
    self.openingTime = openingTime
    self.closingTime = closingTime
    self.managerId = managerId