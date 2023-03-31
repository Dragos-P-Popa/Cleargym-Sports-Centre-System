from app import app, db, models, mail
import availability
from availability import Booking
# Do not forget to import Flask when you need it.
from flask import json, request, jsonify, abort
from datetime import datetime, time, date, timedelta
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
import requests
from flask_mail import Mail, Message


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
    user_input = request.get_json()

    # Getting all booking in the Database and count them
    all_bookings = models.Booking.query.all()
    bookingId = len(all_bookings) + 1

    # Giving the booking a booking ID automatically
    for item in all_bookings:
        if models.Booking.query.get(bookingId):
            bookingId = bookingId - 1
        elif models.Booking.query.get(bookingId):
            bookingId = bookingId + 1

    # Calculating the end_time
    booking_start_time = datetime.strptime(user_input['bookingTime'], '%H:%M').time()
    booking_length = datetime.strptime(user_input['bookingLength'], '%H:%M').time()
    booking_end_time = (datetime.combine(datetime.today(), booking_start_time) +
                        timedelta(hours=booking_length.hour,
                                  minutes=booking_length.minute,
                                  seconds=booking_length.second)).time()

    # Create a new booking
    try:
        booking = models.Booking(
            id=bookingId,
            userId=user_input["userId"],
            facilityId=user_input["facilityId"],
            activityId=user_input["activityId"],
            bookingDate=datetime.strptime(user_input["bookingDate"], '%Y/%m/%d').date(),
            bookingTime=booking_start_time,
            bookingLength=booking_length,
            bookingEndTime=booking_end_time
        )

        # Getting the facility and activity ID values from the user new booking
        facilityId = booking.facilityId
        activityId = booking.activityId

        # Getting the facility details from facilities API
        facility_link = requests.get(f"http://127.0.0.1:3003/facility/{facilityId}")
        # facility_link = requests.get(f"http://cleargym.live:3003/facility/{facilityId}")

        facility_details = facility_link.json()
        facility_open_time = datetime.strptime(facility_details['openingTime'], '%H:%M:%S').time()
        f_closeTime = datetime.strptime(facility_details['closingTime'], '%H:%M:%S').time()
        f_capacity = facility_details['capacity']

        # Getting the activity details from facilities API
        activity_link = requests.get(f"http://127.0.0.1:3003/activity/{activityId}")
        # activity_link = requests.get(f"http://cleargym.live:3003/activity/{activityId}")

        activity_details = activity_link.json()
        a_open = activity_details['activityStartTime']
        a_close = activity_details['activityEndTime']
        a_openTime = datetime.strptime(a_open, '%H:%M').time()
        a_closeTime = datetime.strptime(a_close, '%H:%M').time()
        a_day = activity_details['activityDay']

        a_length = (datetime.combine(datetime.today(), a_closeTime) -
                    timedelta(hours=a_openTime.hour,
                              minutes=a_openTime.minute,
                              seconds=a_openTime.second)).time()

        # Calling the Availability Class and its functions to check the booking.
        b = Booking(booking.bookingDate,
                    booking.bookingTime,
                    booking.bookingLength,
                    booking.bookingEndTime,
                    facilityId,
                    f_closeTime,
                    facility_open_time,
                    f_capacity,
                    a_openTime,
                    a_closeTime,
                    a_length,
                    a_day
                    )

        # Check Facilities Begin
        check_facility_time(b, f_closeTime, facility_open_time, booking)
        check_facility_capacity(b, facilityId, booking, f_capacity)
        # Check Facilities Done

        # Check Activities Begin
        b.check_activity(a_length,
                         a_day,
                         booking.bookingLength,
                         booking.bookingDate,
                         booking.bookingTime,
                         booking.bookingEndTime,
                         a_openTime,
                         a_closeTime
                         )

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
    respo = []
    # Get the current year
    current_year = datetime.now().year
    # Create a date object with the given month, day, and current year
    mydate = date(current_year, month, day)
    # daily results is a list of boolean variables for each hour in a day
    daily_results = []
    # one_hour is an amount of time
    one_hour = time(1, 0, 0)
    # request facility
    facility_link = requests.get(f"http://127.0.0.1:3003/facility/{facilityId}")
    facility_details = facility_link.json()
    f_openTime = datetime.strptime(facility_details['openingTime'], '%H:%M:%S').time()
    f_closeTime = datetime.strptime(facility_details['closingTime'], '%H:%M:%S').time()
    f_capacity = facility_details['capacity']
    # Convert the facility start and end time hours to integers
    start = int(f_openTime.strftime('%H'))
    end = int(f_closeTime.strftime('%H'))
    # Getting the end hour and add 1 to it ( to be used in the loop )
    end_plus = end + 1

    for hour in range(start, end_plus):

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
        booking = b1 + b2 + b3
        # the_hour = current_time.strftime("%H:%M:%S")
        # the_time = "Time : "
        # result1 = the_time + the_hour
        # the_status = "Availability"
        data = {}
        data["Hour"] = hour
        if booking > f_capacity:
            status = False
            data["Availability"] = status
            respo.append(data)
        else:
            status = True
            # result2 = the_status + str(status)
            # daily_results.append([result1, result2])
            data["Availability"] = status
            respo.append(data)

    return jsonify(respo), 200


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
    facility_link = requests.get(f"http://127.0.0.1:3003/facility/{facilityId}")
    facility_details = facility_link.json()
    f_openTime = datetime.strptime(facility_details['openingTime'], '%H:%M:%S').time()
    f_closeTime = datetime.strptime(facility_details['closingTime'], '%H:%M:%S').time()
    f_capacity = facility_details['capacity']

    # Convert the facility start and end time hours to integers
    start = int(f_openTime.strftime('%H'))
    end = int(f_closeTime.strftime('%H'))

    # Getting the end hour and add 1 to it ( to be used in the 2 nd loop )
    end_plus = end + 1

    # Convert the first and last days in a month to ints
    first_day = start_date.day
    last_day = end_date.day

    # Getting the Last day and add 1 day to it ( to be used in the 1 st loop )
    last_day_plus = last_day + 1

    for day in range(first_day, last_day_plus):

        for hour in range(start, end_plus):
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

            booking = b1 + b2 + b3
        if booking > f_capacity:
            status = False
            daily_results.append(status)
        else:
            status = True
            daily_results.append(status)

    retValue = []

    # for item in daily_results:
    for number in range(first_day, last_day + 1):
        data = {}
        data["Day"] = number

        if False not in daily_results:
            day_availability = True
            data["Availability"] = day_availability
            retValue.append(data)
        elif True not in daily_results:
            day_availability = False
            data["Availability"] = day_availability
            retValue.append(data)

    return jsonify(retValue), 200


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


def check_facility_time(b, closeTime, openTime, booking):
    b.check_facility_time(booking.bookingTime,
                          booking.bookingEndTime,
                          openTime,
                          closeTime)


def check_facility_capacity(b, f_id, booking, capacity):
    b.check_facility_capacity(booking.bookingDate,
                              booking.bookingTime,
                              booking.bookingEndTime,
                              f_id,
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


@app.route('/emails/confirmation/<email>', methods=['POST'])
def Email_confirmation(email):
    Sub = "Get ready! Your session is booked"
    Sender = "cleargymstaff@gmail.com"
    Recipient = [email]
    Body = f'''Dear User,

Thank you for booking a session through our app. We are excited to have you as a customer and look forward to providing you with a great experience.

If you need to cancel or reschedule your session, please let us know or use our app.

If you have any questions or concerns, please do not hesitate to contact us. We are always here to help.

Thank you again for choosing our app for your booking needs. We hope you enjoy your session!

Best regards,

Cleargym Team
    '''
    message = Message(Sub,
                      sender=Sender,
                      recipients=Recipient)
    print(type(message))
    message.body = Body

    try:
        mail.send(message)
        return jsonify("Sent")
    except Exception as e:
        print(e)
        return jsonify("Failed")


@app.route('/emails/cancellation/<email>', methods=['POST'])
def Email_cancellation(email):
    Sub = "Cancellation of your session booking"
    Sender = "cleargymstaff@gmail.com"
    Recipient = [email]
    Body = f'''Dear User,

We're sorry to hear that you need to cancel your session booking. We understand that circumstances can change, and we're here to help make the cancellation process as easy as possible for you.

If you would like to proceed with the cancellation, please reply to this email and let us know.

We will process your cancellation request as soon as possible.

If you have any questions or concerns, please do not hesitate to contact us. We are always here to help.

Thank you for using our booking app, and we hope to have the opportunity to serve you again in the future.

Best regards,

    '''
    message = Message(Sub,
                      sender=Sender,
                      recipients=Recipient)
    print(type(message))
    message.body = Body

    try:
        mail.send(message)
        return jsonify("Sent")
    except Exception as e:
        print(e)
        return jsonify("Failed")
