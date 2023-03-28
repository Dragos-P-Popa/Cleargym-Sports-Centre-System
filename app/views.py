from app import app, db, models
import availability
from availability import Booking
# Do not forget to import Flask when you need it.
from flask import json, request, jsonify, abort
from datetime import datetime, time, date, timedelta
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
import requests


# pip freeze > booking_requirements.txt

############################### ERROR HANDLERS ###############################


# The error handling was implemented and debugged
# with the help of the following documentation and thread
# https://flask.palletsprojects.com/en/2.2.x/errorhandling/#returning-api-errors-as-json
# https://stackoverflow.com/questions/24522290/cannot-catch-sqlalchemy-integrityerror

# The error handlers for IntegrityError, KeyError, UnmappedInstanceError,
# TypeError, AttributeError and ValueError.
# These might occur when data is:
# - of an invalid type from the database schema perspective
# - missing from the request
# - refers to a non-existent database record
# - of an invalid type as a function parameter
# - refering to a non-existent attribute, e.g. in a NoneType object
# - sent in an incorrect format (e.g. date/time)


@app.errorhandler(IntegrityError)
def integrity_error_handler(error):
    db.session.rollback()
    app.logger.error(str(error))
    # IntegrityError refers to invalid data type in database operations
    return jsonify({"IntegrityError": "Invalid data in one or more fields"}), 400


@app.errorhandler(KeyError)
def key_error_handler(error):
    db.session.rollback()
    app.logger.error(str(error))
    # KeyError refers to a missing key:value pair
    return jsonify({"KeyError": "Missing data in the request"}), 400


@app.errorhandler(UnmappedInstanceError)
def unmapped_error_handler(error):
    db.session.rollback()
    app.logger.error("UnmappedInstanceError detected")
    # UnmappedInstanceError is raised when trying to operate on a non-existent record
    return jsonify({"UnmappedInstanceError": "Record not found in the database"}), 400


@app.errorhandler(TypeError)
def type_error_handler(error):
    db.session.rollback()
    app.logger.error("TypeError detected")
    # TypeError refers to invalid data type passed as an argument to a function
    return jsonify({"TypeError": "Endpoint function operating on a wrong data type"}), 400


@app.errorhandler(AttributeError)
def attribute_error_handler(error):
    db.session.rollback()
    app.logger.error("AttributeError detected")
    # AttributeError is raised when trying to access an attribute
    # of a NoneType object assigned to a variable in views.py
    return jsonify({"AttributeError": "The referenced record does not exist"}), 400


@app.errorhandler(ValueError)
def value_error_handler(error):
    db.session.rollback()
    app.logger.error("ValueError detected")
    # ValueError is raised when the sent data does not match the required format
    # e.g. date/time
    return jsonify({"ValueError": "Data does not match the required format in one or more fields"}), 400


########################### BOOKING TABLE END POINTS ###########################


# This function is to create a new booking
@app.route('/booking', methods=['POST'])
def post_booking():
    # requesting the data
    info = request.get_json()

    # Getting all booking in the Database and count them
    all_bookings = models.Booking.query.all()
    ID = len(all_bookings) + 1

    # Giving the booking a booking ID automatically
    for item in all_bookings:
        if models.Booking.query.get(ID):
            ID = ID - 1
        elif models.Booking.query.get(ID):
            ID = ID + 1

    # Calculating the end_time
    start = datetime.strptime(info['bookingTime'], '%H:%M').time()
    length = datetime.strptime(info['bookingLength'], '%H:%M').time()
    x = (datetime.combine(datetime.today(), start) +
         timedelta(hours=length.hour,
                   minutes=length.minute,
                   seconds=length.second)).time()
    print("Test 1")
    # Create a new booking
    try:
        booking = models.Booking(
            # createDate: default in models.py
            id=ID,
            userId=info["userId"],
            facilityId=info["facilityId"],
            activityId=info["activityId"],
            bookingDate=datetime.strptime(info["bookingDate"], '%Y/%m/%d').date(),
            bookingTime=start,
            bookingLength=length,
            bookingEndTime=x
        )
        print("Test 2")
        # Getting the facility and activity ID values from the user new booking
        F_id = booking.facilityId
        A_id = booking.activityId

        # Getting the facility details from facilities API
        Facility_link = requests.get(f"http://127.0.0.1:3003/facility/{F_id}")
        Facility_details = Facility_link.json()
        F_OpenTime = datetime.strptime(Facility_details['openingTime'], '%H:%M:%S').time()
        F_CloseTime = datetime.strptime(Facility_details['closingTime'], '%H:%M:%S').time()
        F_capacity = Facility_details['capacity']
        print("Test 3")
        # Getting the activity details from facilities API
        Activity_link = requests.get(f"http://127.0.0.1:3003/activity/{A_id}")  #
        Activity_details = Activity_link.json()
        A_Open = Activity_details['activityStartTime']
        A_Close = Activity_details['activityEndTime']
        A_OpenTime = datetime.strptime(A_Open, '%H:%M').time()
        A_CloseTime = datetime.strptime(A_Close, '%H:%M').time()
        A_day = Activity_details['activityDay']
        print("Test 4")
        Alength = (datetime.combine(datetime.today(), A_CloseTime) -
                   timedelta(hours=A_OpenTime.hour,
                             minutes=A_OpenTime.minute,
                             seconds=A_OpenTime.second)).time()
        print("Test 5")
        # Calling the Availability Class and its functions to check the booking.
        B = Booking(booking.bookingDate,
                    booking.bookingTime,
                    booking.bookingLength,
                    booking.bookingEndTime,
                    F_id,
                    F_CloseTime,
                    F_OpenTime,
                    F_capacity,
                    A_OpenTime,
                    A_CloseTime,
                    Alength,
                    A_day
                    )
        print("Test 6")
        # Check Facilities Begin
        check_facility_time(B, F_CloseTime, F_OpenTime, booking)
        check_facility_capacity(B, F_id, booking, F_capacity)
        # Check Facilities Done
        print("Test 7")
        # Check Activities Begin
        print(A_OpenTime)
        print(A_CloseTime)
        print(Alength)
        print(A_day)
        B.check_activity(Alength,
                         A_day,
                         booking.bookingLength,
                         booking.bookingDate,
                         booking.bookingTime,
                         booking.bookingEndTime,
                         A_OpenTime,
                         A_CloseTime
                         )
        print("Test 8")
        # Check Activities Done
        # add and commit the booking details to the database (Booking.db)
        db.session.add(booking)
        db.session.commit()

        # Create a new response
        response = get_response_for_post(booking)

    # Check for possible errors in the submitted data
    except (IntegrityError, KeyError, UnmappedInstanceError, TypeError, ValueError) as error:
        raise error

    # Return the response
    return jsonify(response), 200


@app.route('/availability/<int:facilityId>/<int:month>/<int:day>', methods=['GET'])
def get_daily_availability(facilityId, month, day):
    # Get the current year
    current_year = datetime.now().year
    # Create a date object with the given month, day, and current year
    mydate = date(current_year, month, day)
    # daily results is a list of boolean variables for each hour in a day
    daily_results = []
    # one_hour is an amount of time
    one_hour = time(1, 0, 0)
    # request facility
    Facility_link = requests.get(f"http://127.0.0.1:3003/facility/{facilityId}")
    Facility_details = Facility_link.json()
    F_OpenTime = datetime.strptime(Facility_details['openingTime'], '%H:%M:%S').time()
    F_CloseTime = datetime.strptime(Facility_details['closingTime'], '%H:%M:%S').time()
    F_capacity = Facility_details['capacity']
    # Convert the facility start and end time hours to integers
    Start = int(F_OpenTime.strftime('%H'))
    End = int(F_CloseTime.strftime('%H'))
    # Getting the end hour and add 1 to it ( to be used in the loop )
    end_plus = End + 1

    for hour in range(Start, end_plus):

        current_time = time(hour, 0)

        next_time = (datetime.combine(datetime.today(), current_time)
                     + timedelta(hours=one_hour.hour, minutes=one_hour.minute, seconds=one_hour.second)).time()

        bookings = models.Booking.query.filter_by(
            bookingDate=mydate,
            bookingTime=current_time,
            bookingEndTime=next_time,
            facilityId=facilityId).all()

        # All Bookings that starts at booking current time of that facility.
        a1 = models.Booking.query.filter_by(bookingDate=mydate,
                                            bookingTime=current_time,
                                            facilityId=facilityId).all()

        # All Bookings that starts booking start time and ends in one hour
        a2 = models.Booking.query.filter_by(bookingDate=mydate,
                                            bookingTime=current_time,
                                            bookingEndTime=next_time,
                                            facilityId=facilityId
                                            ).all()

        # All bookings that ends after 1 hour of booking start time
        a3 = models.Booking.query.filter_by(bookingDate=mydate,
                                            bookingEndTime=next_time,
                                            facilityId=facilityId
                                            ).all()
        b1 = len(a1)
        b2 = len(a2)
        b3 = len(a3)
        # space = " "
        timing = current_time.strftime("%H:%M:%S")
        # data = timing + space + str(status)

        booking = b1 + b2 + b3
        if booking > F_capacity:
            status = False
            daily_results.append([timing, status])
        else:
            status = True
            daily_results.append([timing, status])

    return jsonify(daily_results), 200


@app.route('/availability/<int:facilityId>/<int:month>', methods=['GET'])
def get_monthly_availability(facilityId, month):
    # Get the current year
    current_year = datetime.now().year

    # The first day of the month
    start_date = date(current_year, month, 1)

    # get the number of days in the month
    num_days = (date(current_year, month + 1, 1) - date(current_year, month, 1)).days

    # The last day in the month
    end_date = date(current_year, month, num_days)

    # daily results is a list of boolean variables for each hour in a day
    daily_results = []

    # monthly results is a list of boolean variables for each day in a month
    monthly_results = []

    # one_hour is an amount of time
    one_hour = time(1, 0, 0)

    # request facility
    Facility_link = requests.get(f"http://127.0.0.1:3003/facility/{facilityId}")
    Facility_details = Facility_link.json()
    F_OpenTime = datetime.strptime(Facility_details['openingTime'], '%H:%M:%S').time()
    F_CloseTime = datetime.strptime(Facility_details['closingTime'], '%H:%M:%S').time()
    F_capacity = Facility_details['capacity']

    # Convert the facility start and end time hours to integers
    Start = int(F_OpenTime.strftime('%H'))
    End = int(F_CloseTime.strftime('%H'))

    # Getting the end hour and add 1 to it ( to be used in the 2 nd loop )
    end_plus = End + 1

    # Convert the first and last days in a month to ints
    First_day = start_date.day
    Last_day = end_date.day

    # Getting the Last day and add 1 day to it ( to be used in the 1 st loop )
    Last_day_plus = Last_day + 1

    for day in range(First_day, Last_day_plus):

        for hour in range(Start, end_plus):
            current_time = time(hour, 0)

            next_time = (datetime.combine(datetime.today(), current_time)
                         + timedelta(hours=one_hour.hour, minutes=one_hour.minute, seconds=one_hour.second)).time()

            bookings = models.Booking.query.filter_by(
                bookingDate=day,
                bookingTime=current_time,
                bookingEndTime=next_time,
                facilityId=facilityId).all()

            # All Bookings that starts at booking current time of that facility.
            a1 = models.Booking.query.filter_by(bookingDate=day,
                                                bookingTime=current_time,
                                                facilityId=facilityId).all()

            # All Bookings that starts booking start time and ends in one hour
            a2 = models.Booking.query.filter_by(bookingDate=day,
                                                bookingTime=current_time,
                                                bookingEndTime=next_time,
                                                facilityId=facilityId
                                                ).all()

            # All bookings that ends after 1 hour of booking start time
            a3 = models.Booking.query.filter_by(bookingDate=day,
                                                bookingEndTime=next_time,
                                                facilityId=facilityId
                                                ).all()
            b1 = len(a1)
            b2 = len(a2)
            b3 = len(a3)
            # space = " "
            timing = current_time.strftime("%H:%M:%S")
            # data = timing + space + str(status)

            booking = b1 + b2 + b3
        if booking > F_capacity:
            status = False
            daily_results.append([timing, status])
        else:
            status = True
            daily_results.append([timing, status])

    for item in daily_results:
        if False not in daily_results:
            day_availability = True
            monthly_results.append(day_availability)
        elif True not in daily_results:
            day_availability = False
            monthly_results.append(day_availability)

    return jsonify(monthly_results), 200


# This function is to delete a booking by using the booking id
@app.route('/bookings/<int:id>', methods=['DELETE'])
def delete_booking(id):
    try:
        # requesting the data from the database by using the selected booking id
        booking = models.Booking.query.get(id)

        # delete and commit the booking details from the database (Booking.db)
        db.session.delete(booking)
        db.session.commit()

        # Create a new response
        response = {'id': booking.id,
                    'userId': booking.userId,
                    'facilityId': booking.facilityId,
                    'activityId': booking.activityId,
                    'createDate': booking.createDate.strftime('%Y/%m/%d'),
                    'bookingDate': booking.bookingDate.strftime('%Y/%m/%d'),
                    'bookingTime': booking.bookingTime.strftime('%H:%M'),
                    'bookingLength': booking.bookingLength.strftime('%H:%M'),
                    'bookingEndTime': booking.bookingEndTime.strftime('%H:%M')
                    }

    # Check for possible errors in the submitted data
    except (IntegrityError, KeyError, UnmappedInstanceError, TypeError, ValueError) as error:
        raise error

    # Return the response
    return jsonify(response), 200


# This function is to show all bookings of a user by using the user id
@app.route('/bookings/user/<userId>', methods=['GET'])
def get_booking_uid(userId):
    try:
        # Booking_Time = post_booking(booking.bookingTime)
        # requesting all bookings from the database by using the selected user id
        bookings = models.Booking.query.filter_by(userId=userId).all()

        booking_list = []

        for booking in bookings:
            # Adding all bookings in a list called booking_list
            booking_list.append({
                'id': booking.id,
                'userId': booking.userId,
                'facilityId': booking.facilityId,
                'activityId': booking.activityId,
                'createDate': booking.createDate.strftime('%Y/%m/%d'),
                'bookingDate': booking.bookingDate.strftime('%Y/%m/%d'),
                'bookingTime': booking.bookingTime.strftime('%H:%M'),
                'bookingLength': booking.bookingLength.strftime('%H:%M'),
                'bookingEndTime': booking.bookingEndTime.strftime('%H:%M')
            })

    # Check for possible errors in the submitted data
    except (IntegrityError, KeyError, UnmappedInstanceError, TypeError, ValueError) as error:
        raise error

    # Return the response ( The booking_list )
    return jsonify(booking_list), 200


# This function is to get a booking by using the booking id
@app.route('/bookings/<int:id>', methods=['GET'])
def get_booking_bid(id):
    try:
        # Requesting the data from the database by using the selected booking id
        booking = models.Booking.query.get(id)

        # Create a new response
        response = {'id': booking.id,
                    'userId': booking.userId,
                    'facilityId': booking.facilityId,
                    'activityId': booking.activityId,
                    'createDate': booking.createDate.strftime('%Y/%m/%d'),
                    'bookingDate': booking.bookingDate.strftime('%Y/%m/%d'),
                    'bookingTime': booking.bookingTime.strftime('%H:%M'),
                    'bookingLength': booking.bookingLength.strftime('%H:%M'),
                    'bookingEndTime': booking.bookingEndTime.strftime('%H:%M')
                    }

    # Check for possible errors in the submitted data
    except (IntegrityError, KeyError, UnmappedInstanceError, TypeError, ValueError) as error:
        raise error

    # Return the response
    return jsonify(response), 200


# This function is to patch a booking by using the booking id
@app.route('/bookings/<int:id>', methods=['PATCH'])
def patch_booking(id):
    try:
        # Requesting the data from the database by using the selected booking id
        booking = models.Booking.query.get(id)

        # Decoding the data sent to the API
        request_data = request.get_json()

        # Iterate over the key, value pairs in the request data
        for attribute, value in request_data.items():

            # Validate which attribute is being updated
            # and execute the corresponding code
            if attribute == "userId":
                booking.userId = value
            elif attribute == "facilityId":
                booking.facilityId = value
            elif attribute == "activityId":
                booking.activityId = value
            elif (attribute == "bookingDate"):
                setattr(booking, attribute, datetime.strptime(value, '%Y/%m/%d').date())
            elif (attribute == "bookingTime"):
                start = datetime.strptime(value, '%H:%M').time()
                booking.bookingTime = start
                length = booking.bookingLength
                booking.bookingEndTime = (datetime.combine(datetime.today(), start) +
                                          timedelta(hours=length.hour,
                                                    minutes=length.minute)).time()
            elif (attribute == "bookingLength"):
                start = booking.bookingTime
                length = datetime.strptime(value, '%H:%M').time()
                booking.bookingLength = length
                booking.bookingEndTime = (datetime.combine(datetime.today(), start) +
                                          timedelta(hours=length.hour,
                                                    minutes=length.minute)).time()

        # Commit the changes made
        db.session.commit()

        # Create a new response
        response = {'id': booking.id,
                    'userId': booking.userId,
                    'facilityId': booking.facilityId,
                    'activityId': booking.activityId,
                    'createDate': booking.createDate.strftime('%Y/%m/%d'),
                    'bookingDate': booking.bookingDate.strftime('%Y/%m/%d'),
                    'bookingTime': booking.bookingTime.strftime('%H:%M'),
                    'bookingLength': booking.bookingLength.strftime('%H:%M'),
                    'bookingEndTime': booking.bookingEndTime.strftime('%H:%M')
                    }

    # Check for possible errors in the submitted data
    except (IntegrityError, KeyError, UnmappedInstanceError, TypeError, ValueError) as error:
        raise error

    # Return the response
    return jsonify(response), 200


def check_facility_time(B, CloseTime, OpenTime, booking):
    B.check_facility_time(booking.bookingTime,
                          booking.bookingEndTime,
                          OpenTime,
                          CloseTime)


def check_facility_capacity(B, F_id, booking, capacity):
    B.check_facility_capacity(booking.bookingDate,
                              booking.bookingTime,
                              booking.bookingEndTime,
                              F_id,
                              capacity,
                              booking.bookingLength)


def get_response_for_post(booking):
    return {'id': booking.id,
            'userId': booking.userId,
            'facilityId': booking.facilityId,
            'activityId': booking.activityId,
            'createDate': booking.createDate.strftime('%Y/%m/%d'),
            'bookingDate': booking.bookingDate.strftime('%Y/%m/%d'),
            'bookingTime': booking.bookingTime.strftime('%H:%M'),
            'bookingLength': booking.bookingLength.strftime('%H:%M'),
            'bookingEndTime': booking.bookingEndTime.strftime('%H:%M')
            }
