from app import db

#association_table = db.Table(
 #   "association_table",
 #   db.Model.metadata,
  #  db.Column("facilityID",
     #         db.ForeignKey("facility_table.id", ondelete="CASCADE"),
      #       primary_key=True),
    #db.Column("activityID",
     #         db.ForeignKey("activity_table.activityId", ondelete="CASCADE"),
     #         primary_key=True),
#)

class Association(db.Model):
    __tablename__ = "association_table"
    facilityID = db.Column(db.Integer, db.ForeignKey('facility_table.id'), nullable=False , primary_key=True)
    activityID = db.Column(db.Integer, db.ForeignKey('activity_table.activityId'), nullable=False, primary_key=True)



# the Facilities table represents facilities in the Sports Centre
class Facility(db.Model):
    __tablename__ = "facility_table"
    # id attribute is a primary key for Facility model
    id = db.Column(db.Integer, primary_key=True)
    # the following attributes can not be left empty, therefore nullable=False
    facilityName = db.Column(db.String(500), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    openingTime = db.Column(db.Time, nullable=False)
    closingTime = db.Column(db.Time, nullable=False)
    managerId = db.Column(db.String, nullable=False)
    # Set up a many-to-many relationship between Facilities and their Activities
    activity = db.relationship("Activity",
                               secondary="association_table",
                               back_populates="facility",
                               lazy='dynamic')


# The model of the Activity table
class Activity(db.Model):
    __tablename__ = "activity_table"
    activityId = db.Column(db.Integer, primary_key=True, nullable=False)
    activityType = db.Column(db.String(100), nullable=False)
    activityStartTime = db.Column(db.Time, nullable=False)
    activityEndTime = db.Column(db.Time, nullable=False)
    activityDay = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float, nullable=False, default=14)
    productId = db.Column(db.Integer, nullable=False, default=14)
    # Set up a many-to-many relationship between Facilities and their Activities
    facility = db.relationship("Facility",
                               secondary="association_table",
                               back_populates="activity",
                               lazy='dynamic')

    # The one-to-many relationship set up is explained in more detail in the
    # following SQLAlchemy documentation:
    # https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#many-to-one
    # (It is one activity to many facilities)
