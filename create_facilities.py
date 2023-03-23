from app import db, models, app
from datetime import datetime


def preload_data():
    '''function to preload some data in the database'''

    with app.app_context():
        # create the table and the database
        db.create_all()

################################ RETRIEVE DATA ################################


        # Facility table

        swimming_pool = models.Facility.query.filter_by(
                    facilityName='Swimming pool').first()
        fitness_room = models.Facility.query.filter_by(
                    facilityName='Fitness room').first()
        court_1 = models.Facility.query.filter_by(
                    facilityName='Squash court 1').first()
        court_2 = models.Facility.query.filter_by(
                    facilityName='Squash court 2').first()
        sports_hall = models.Facility.query.filter_by(
                    facilityName='Sports hall').first()
        climbing_wall = models.Facility.query.filter_by(
                    facilityName='Climbing wall').first()
        studio = models.Facility.query.filter_by(
                    facilityName='Studio').first()

        # Activity table

        general_use = models.Activity.query.filter_by(
            activityType='General_use').first()
        lane_swimming = models.Activity.query.filter_by(
            activityType='Lane_swimming').first()
        lessons = models.Activity.query.filter_by(
            activityType='Lessons').first()
        one_hour_session = models.Activity.query.filter_by(
            activityType='One_hour_session').first()
        pilates = models.Activity.query.filter_by(
            activityType='Pilates').first()
        aerobics1 = models.Activity.query.filter_by(
            activityType='Aerobics').first()
        aerobics2 = models.Activity.query.filter_by(
            activityType='Aerobics').offset(1).first()
        aerobics3 = models.Activity.query.filter_by(
            activityType='Aerobics').offset(2).first()
        yoga1 = models.Activity.query.filter_by(
            activityType='Yoga').first()
        yoga2 = models.Activity.query.filter_by(
            activityType='Yoga').offset(1).first()


########################## INITIALISE FACILITIES DATA ##########################


        # create facilities' records if they do not already exist in the table, 
        # gym works 8:00-22:00, 7 days a week with some exceptions
        # swimming pool opened 8:00-20:00
        # climbing wall opened 10:00-20:00
        if not swimming_pool:
            swimming_pool = models.Facility(
                facilityName="Swimming pool", 
                capacity=30, 
                openingTime=datetime.strptime("08:00:00",'%H:%M:%S').time(), 
                closingTime=datetime.strptime("20:00:00", '%H:%M:%S').time(), 
                managerId="2d32wvfnh34")        
        
        if not fitness_room:
            fitness_room = models.Facility(
                facilityName="Fitness room", 
                capacity=35, 
                openingTime=datetime.strptime("08:00:00", '%H:%M:%S').time(), 
                closingTime=datetime.strptime("22:00:00", '%H:%M:%S').time(), 
                managerId="2d32wvfnh34")
        
        if not court_1:    
            court_1 = models.Facility(
                facilityName="Squash court 1", 
                capacity=4, 
                openingTime=datetime.strptime("08:00:00", '%H:%M:%S').time(), 
                closingTime=datetime.strptime("22:00:00", '%H:%M:%S').time(), 
                managerId="2d32wvfnh34")
        
        if not court_2:    
            court_2 = models.Facility(
                facilityName="Squash court 2", 
                capacity=4, 
                openingTime=datetime.strptime("08:00:00", '%H:%M:%S').time(), 
                closingTime=datetime.strptime("22:00:00", '%H:%M:%S').time(), 
                managerId="2d32wvfnh34")
        
        if not sports_hall:    
            sports_hall = models.Facility(
                facilityName="Sports hall", 
                capacity=45, 
                openingTime=datetime.strptime("08:00:00", '%H:%M:%S').time(), 
                closingTime=datetime.strptime("22:00:00", '%H:%M:%S').time(), 
                managerId="2d32wvfnh34")
        
        if not climbing_wall:
            climbing_wall = models.Facility(
                facilityName="Climbing wall", 
                capacity=22, 
                openingTime=datetime.strptime("10:00:00", '%H:%M:%S').time(), 
                closingTime=datetime.strptime("20:00:00", '%H:%M:%S').time(), 
                managerId="2d32wvfnh34")
        
        if not studio:
            studio = models.Facility(
                facilityName="Studio", 
                capacity=25, 
                openingTime=datetime.strptime("08:00:00", '%H:%M:%S').time(), 
                closingTime=datetime.strptime("22:00:00", '%H:%M:%S').time(), 
                managerId="2d32wvfnh34")


########################## INITIALISE ACTIVITIES DATA ##########################


        if not general_use:
            general_use = models.Activity(
                activityType="General use", 
                activityStartTime=datetime.strptime("08:00:00",'%H:%M:%S').time(), 
                activityEndTime=datetime.strptime("22:00:00",'%H:%M:%S').time(), 
                activityDay="Any")

        if not lane_swimming:
            lane_swimming = models.Activity(
                activityType="Lane swimming", 
                activityStartTime=datetime.strptime("08:00:00",'%H:%M:%S').time(), 
                activityEndTime=datetime.strptime("22:00:00",'%H:%M:%S').time(), 
                activityDay="Any")

        if not lessons:
            lessons = models.Activity(
                activityType="Lessons", 
                activityStartTime=datetime.strptime("08:00:00",'%H:%M:%S').time(), 
                activityEndTime=datetime.strptime("22:00:00",'%H:%M:%S').time(), 
                activityDay="Any")

        if not one_hour_session:
            one_hour_session = models.Activity(
                activityType="1-hour session", 
                activityStartTime=datetime.strptime("08:00:00",'%H:%M:%S').time(), 
                activityEndTime=datetime.strptime("22:00:00",'%H:%M:%S').time(), 
                activityDay="Any")

        if not pilates:
            pilates = models.Activity(
                activityType="Pilates", 
                activityStartTime=datetime.strptime("18:00:00",'%H:%M:%S').time(), 
                activityEndTime=datetime.strptime("19:00:00",'%H:%M:%S').time(), 
                activityDay="Monday")

        if not aerobics1:
            aerobics1 = models.Activity(
                activityType="Aerobics", 
                activityStartTime=datetime.strptime("10:00:00",'%H:%M:%S').time(), 
                activityEndTime=datetime.strptime("11:00:00",'%H:%M:%S').time(), 
                activityDay="Tuesday")

        if not aerobics2:
            aerobics2 = models.Activity(
                activityType="Aerobics", 
                activityStartTime=datetime.strptime("19:00:00",'%H:%M:%S').time(), 
                activityEndTime=datetime.strptime("20:00:00",'%H:%M:%S').time(), 
                activityDay="Thursday") 
        
        if not aerobics3:
            aerobics3 = models.Activity(
                activityType="Aerobics", 
                activityStartTime=datetime.strptime("10:00:00",'%H:%M:%S').time(), 
                activityEndTime=datetime.strptime("11:00:00",'%H:%M:%S').time(), 
                activityDay="Saturday")
        
        if not yoga1:
            yoga1 = models.Activity(
                activityType="Yoga", 
                activityStartTime=datetime.strptime("19:00:00",'%H:%M:%S').time(), 
                activityEndTime=datetime.strptime("20:00:00",'%H:%M:%S').time(), 
                activityDay="Friday")
        
        if not yoga2:
            yoga2 = models.Activity(
                activityType="Yoga", 
                activityStartTime=datetime.strptime("09:00:00",'%H:%M:%S').time(), 
                activityEndTime=datetime.strptime("10:00:00",'%H:%M:%S').time(), 
                activityDay="Sunday")


######################## POPULATE THE ASSOCIATION TABLE ########################


        swimming_pool.activity.append(general_use)
        swimming_pool.activity.append(lane_swimming)
        swimming_pool.activity.append(lessons)

        fitness_room.activity.append(general_use)

        court_1.activity.append(one_hour_session)

        court_2.activity.append(one_hour_session)

        sports_hall.activity.append(one_hour_session)

        climbing_wall.activity.append(general_use)

        studio.activity.append(pilates)
        studio.activity.append(aerobics1)
        studio.activity.append(aerobics2)
        studio.activity.append(aerobics3)
        studio.activity.append(yoga1)
        studio.activity.append(yoga2)


######################## POPULATE THE ASSOCIATION TABLE ########################


        # add new facilities to the database

        db.session.add(swimming_pool)
        db.session.add(fitness_room)
        db.session.add(court_1)
        db.session.add(court_2)
        db.session.add(sports_hall)
        db.session.add(climbing_wall)
        db.session.add(studio)

        # add new activities to the database

        db.session.add(general_use)
        db.session.add(lane_swimming)
        db.session.add(lessons)
        db.session.add(one_hour_session)
        db.session.add(pilates)
        db.session.add(aerobics1)
        db.session.add(aerobics2)
        db.session.add(aerobics3)
        db.session.add(yoga1)
        db.session.add(yoga2)

        # commit changes to the database
        db.session.commit()
