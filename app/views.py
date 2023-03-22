from app import app, db, models
import availability
from availability import Booking
# Do not forget to import Flask when you need it.
from flask import json, request, jsonify, abort
from datetime import datetime, time, date, timedelta
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
import requests


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

    # Create a new booking
    try:
        booking = models.Booking(            
            id=ID,
            userId=info["userId"],
            facilityId=info["facilityId"],
            activityId=info["activityId"],
            # createDate: default in models.py
            bookingDate=datetime.strptime(info["bookingDate"], '%Y/%m/%d').date(),
            bookingTime=start,
            bookingLength=length,
            bookingEndTime=x
        )

        # Getting the facility details from facilities API

        # Getting the facility value from the user new booking
        f_id = booking.facilityId

        # Getting the facility details from facilities API.
        # The first 'facility_link' variable is used for local testing.
        # The other, for remote testing on GitHub.

        # facility_link = requests.get(f"http://127.0.0.1:3003/facility/{f_id}")
        facility_link = requests.get(f"http://cleargym.live:3003/facility/{f_id}")

        facility_details = facility_link.json()

        open_time = facility_details['openingTime']
        close_time = facility_details['closingTime']

        openTime = datetime.strptime(open_time, '%H:%M:%S').time()
        closeTime = datetime.strptime(close_time, '%H:%M:%S').time()
        capacity = facility_details['capacity']

        # Calling the Availability Class and its functions to check the booking.
        # Check Facilities Begin
        # Create a new object:
        b = Booking(booking.bookingDate,
                    booking.bookingTime,
                    booking.bookingLength,
                    booking.bookingEndTime,
                    f_id,
                    closeTime,
                    openTime,
                    capacity)

        b.check_time(booking.bookingTime,
                     booking.bookingEndTime,
                     openTime,
                     closeTime)

        b.check_length(booking,
                       booking.bookingTime,
                       booking.bookingLength,
                       booking.bookingEndTime,
                       capacity,
                       f_id)

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
