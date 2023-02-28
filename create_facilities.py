from app import db, models, app
from datetime import datetime


# function to preload some data in the database
def preload_data():
    with app.app_context():
        # create the table and the database
        db.create_all()

        # create facilities' records, gym works 8:00-22:00, 7 days a week with some exceptions
        # swimming pool opened 8:00-20:00
        swimming_pool = models.Facility(id=1, facilityName="Swimming pool", capacity=30, openingTime=datetime.strptime("08:00:00", '%H:%M:%S').time(), closingTime=datetime.strptime("20:00:00", '%H:%M:%S').time(), managerId="2d32wvfnh34")
        fitness_room = models.Facility(id=2, facilityName="Fitness room", capacity=35, openingTime=datetime.strptime("08:00:00", '%H:%M:%S').time(), closingTime=datetime.strptime("22:00:00", '%H:%M:%S').time(), managerId="2d32wvfnh34")
        court_1 = models.Facility(id=3, facilityName="Squash court 1", capacity=4, openingTime=datetime.strptime("08:00:00", '%H:%M:%S').time(), closingTime=datetime.strptime("22:00:00", '%H:%M:%S').time(), managerId="2d32wvfnh34")
        court_2 = models.Facility(id=4, facilityName="Squash court 2", capacity=4, openingTime=datetime.strptime("08:00:00", '%H:%M:%S').time(), closingTime=datetime.strptime("22:00:00", '%H:%M:%S').time(), managerId="2d32wvfnh34")
        sports_hall = models.Facility(id=5, facilityName="Sports hall", capacity=45, openingTime=datetime.strptime("08:00:00", '%H:%M:%S').time(), closingTime=datetime.strptime("22:00:00", '%H:%M:%S').time(), managerId="2d32wvfnh34")
        # climbing wall opened 10:00-20:00
        climbing_wall = models.Facility(id=6, facilityName="Climbing wall", capacity=22, openingTime=datetime.strptime("10:00:00", '%H:%M:%S').time(), closingTime=datetime.strptime("20:00:00", '%H:%M:%S').time(), managerId="2d32wvfnh34")
        studio = models.Facility(id=7, facilityName="Studio", capacity=25, openingTime=datetime.strptime("08:00:00", '%H:%M:%S').time(), closingTime=datetime.strptime("22:00:00", '%H:%M:%S').time(), managerId="2d32wvfnh34")


        # add new facilities to the database
        db.session.add(swimming_pool)
        db.session.add(fitness_room)
        db.session.add(court_1)
        db.session.add(court_2)
        db.session.add(sports_hall)
        db.session.add(climbing_wall)
        db.session.add(studio)

        # commit changes to the database
        db.session.commit()
