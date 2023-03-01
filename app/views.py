from app import app, db, models
from flask import json, request, jsonify
import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from datetime import datetime

# The error handlers for IntegrityError and KeyError, which might occur when
# data is missing or invalid
@app.errorhandler(IntegrityError)
def integrity_error_handler(error):
    db.session.rollback()
    app.logger.error(str(error))
    return jsonify({"Error": "Invalid or missing data in one or more fields"}), 400

@app.errorhandler(KeyError)
def key_error_handler(error):
    db.session.rollback()
    app.logger.error(str(error))
    return jsonify({"Error": "No data in the request"}), 400

@app.errorhandler(UnmappedInstanceError)
def unmapped_error_handler(error):
    db.session.rollback()
    app.logger.error("UnmappedInstanceError detected")
    return jsonify({"Error": "Invalid ID in the request"}), 400

# This function is to create a new booking
@app.route('/booking', methods=['POST'])
def post_booking():
    # requesting the data
    info = request.get_json()

    # Create a new booking
    try:
        booking = models.Booking(

            id=info["id"],
            userId=info["userId"],
            createDate=datetime.strptime(info["createDate"], '%Y/%m/%d').date(),
            bookingDate=datetime.strptime(info["bookingDate"], '%Y/%m/%d').date(),
            bookingTime=datetime.strptime(info['bookingTime'], '%H:%M').time(),
            bookingLength=datetime.strptime(info['bookingLength'], '%H:%M').time(),
            bookingType=info["bookingType"],
            teamEvent=info["teamEvent"]
        )

        # add and commit the booking details to the database (Booking.db)
        db.session.add(booking)
        db.session.commit()

    # Validate whether any data was submitted and if it is in a valid format

    # The error handling was implemented and debugged
    # with the help of the following documentation and thread
    # https://flask.palletsprojects.com/en/2.2.x/errorhandling/#returning-api-errors-as-json
    # https://stackoverflow.com/questions/24522290/cannot-catch-sqlalchemy-integrityerror
    except IntegrityError:
        raise IntegrityError("IntegrityError detected", IntegrityError, None)

    except KeyError:
        raise KeyError("KeyError detected")

    # Create a new response
    response = {'id': booking.id,
                'userId': booking.userId,
                'createDate': booking.createDate.strftime('%Y/%m/%d'),
                'bookingDate': booking.bookingDate.strftime('%Y/%m/%d'),
                'bookingTime': booking.bookingTime.strftime('%H:%M'),
                'bookingLength': booking.bookingLength.strftime('%H:%M'),
                'bookingType': booking.bookingType,
                'teamEvent': booking.teamEvent
                }

    # return the response
    return jsonify(response), 200


# This function is to delete a booking by using the booking id
@app.route('/bookings/<int:id>', methods=['DELETE'])
def delete_booking(id):

    try:
        # requesting the data from the database by using the selected booking id
        booking = models.Booking.query.get(id)

        # delete and commit the booking details from the database (Booking.db)
        db.session.delete(booking)
        db.session.commit()

    # Validate whether any data was submitted and if it is in a valid format
    except IntegrityError:
        raise IntegrityError("IntegrityError detected", IntegrityError, None)

    except KeyError:
        raise KeyError("KeyError detected")

    except UnmappedInstanceError:
        raise UnmappedInstanceError("UnmappedInstanceError detected")

    # Create a new response
    response = {'id': booking.id,
                'userId': booking.userId,
                'createDate': booking.createDate.strftime('%Y/%m/%d'),
                'bookingDate': booking.bookingDate.strftime('%Y/%m/%d'),
                'bookingTime': booking.bookingTime.strftime('%H:%M'),
                'bookingLength': booking.bookingLength.strftime('%H:%M'),
                'bookingType': booking.bookingType,
                'teamEvent': booking.teamEvent
                }

    # return the response
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
                'createDate': booking.createDate.strftime('%Y/%m/%d'),
                'bookingDate': booking.bookingDate.strftime('%Y/%m/%d'),
                'bookingTime': booking.bookingTime.strftime('%H:%M'),
                'bookingLength': booking.bookingLength.strftime('%H:%M'),
                'bookingType': booking.bookingType,
                'teamEvent': booking.teamEvent
            })

    # Validate whether any data was submitted and if it is in a valid format
    except IntegrityError:
        raise IntegrityError("IntegrityError detected", IntegrityError, None)

    except KeyError:
        raise KeyError("KeyError detected")

    except UnmappedInstanceError:
        raise UnmappedInstanceError("UnmappedInstanceError detected")

    # return the response ( The booking_list )
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
                    'createDate': booking.createDate.strftime('%Y/%m/%d'),
                    'bookingDate': booking.bookingDate.strftime('%Y/%m/%d'),
                    'bookingTime': booking.bookingTime.strftime('%H:%M'),
                    'bookingLength': booking.bookingLength.strftime('%H:%M'),
                    'bookingType': booking.bookingType,
                    'teamEvent': booking.teamEvent
                    }

    # Validate whether any data was submitted and if it is in a valid format
    except IntegrityError:
        raise IntegrityError("IntegrityError detected", IntegrityError, None)

    except KeyError:
        raise KeyError("KeyError detected")

    except UnmappedInstanceError:
        raise UnmappedInstanceError("UnmappedInstanceError detected")

    # return the response
    return jsonify(response), 200
