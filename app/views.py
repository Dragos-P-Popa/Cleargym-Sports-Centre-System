# Bouhamadi Mohamed Yanis

from app import app, db, models
# Do not forget to import Flask when you need it.
from flask import request, jsonify
import datetime
from datetime import datetime


# This function is to create a new booking
@app.route('/booking', methods=['POST'])
def post_booking():
    # requesting the data
    Info = request.get_json()
    # Checking if the data is available
    if not Info:
        return jsonify({'message': 'Missing fields'}), 400

    # Create a new booking
    booking = models.booking(

        id=Info["id"],
        userId=Info["userId"],
        createDate=datetime.strptime(Info["createDate"], '%Y/%m/%d').date(),
        bookingDate=datetime.strptime(Info["bookingDate"], '%Y/%m/%d').date(),
        bookingTime=datetime.strptime(Info['bookingTime'], '%H:%M').time(),
        bookingLength=datetime.strptime(Info['bookingLength'], '%H:%M').time(),
        bookingType=Info["bookingType"],
        teamEvent=Info["teamEvent"]
    )

    # add and commit the booking details to the database (Booking.db)
    db.session.add(booking)
    db.session.commit()

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
    return {'booking': response}, 200

# This function is to delete a booking by using the booking id
@app.route('/bookings/<int:id>', methods=['DELETE'])
def delete_booking(id):

    # requesting the data from the database by using the selected booking id
    booking = models.booking.query.get(id)
    # Checking if the data is available
    if not booking:
        return jsonify({'message': 'Booking does not exist'}), 400

    # delete and commit the booking details from the database (Booking.db)
    db.session.delete(booking)
    db.session.commit()

    # Create a new response
    response = {'id': booking.id,
                'userId': booking.userId,
                'createDate': booking.createDate.strftime('%y/%m/%d'),
                'bookingDate': booking.bookingDate.strftime('%y/%m/%d'),
                'bookingTime': booking.bookingTime.strftime('%H:%M'),
                'bookingLength': booking.bookingLength.strftime('%H:%M'),
                'bookingType': booking.bookingType,
                'teamEvent': booking.teamEvent
                }
    # return the response
    return {'booking': response}, 200

# This function is to show all bookings of a user by using the user id
@app.route('/bookings/user/<userId>', methods=['GET'])
def get_booking_uid(userId):

    # requesting all bookings from the database by using the selected user id
    bookings = models.booking.query.filter_by(userId=userId).all()
    # Checking if the data is available
    if not bookings:
        return jsonify({'message': 'Booking does not exist'}), 400

    if bookings:
        booking_list = []
        for booking in bookings:
            # Adding all bookings in a list called booking_list
            booking_list.append({
                'id': booking.id,
                'userId': booking.userId,
                'createDate': booking.createDate.strftime('%y/%m/%d'),
                'bookingDate': booking.bookingDate.strftime('%y/%m/%d'),
                'bookingTime': booking.bookingTime.strftime('%H:%M'),
                'bookingLength': booking.bookingLength.strftime('%H:%M'),
                'bookingType': booking.bookingType,
                'teamEvent': booking.teamEvent
            })
        # return the response ( The booking_list )
        return jsonify(booking_list)

# This function is to get a booking by using the booking id
@app.route('/bookings/<int:id>', methods=['GET'])
def get_booking_bid(id):
    # requesting the data from the database by using the selected booking id
    booking = models.booking.query.get(id)
    # Checking if the data is available
    if not booking:
        return jsonify({'message': 'Booking does not exist'}), 400

    # Create a new response
    response = {'id': booking.id,
                'userId': booking.userId,
                'createDate': booking.createDate.strftime('%y/%m/%d'),
                'bookingDate': booking.bookingDate.strftime('%y/%m/%d'),
                'bookingTime': booking.bookingTime.strftime('%H:%M'),
                'bookingLength': booking.bookingLength.strftime('%H:%M'),
                'bookingType': booking.bookingType,
                'teamEvent': booking.teamEvent
                }

    # return the response
    return {'booking': response}, 200


# To be done soon
@app.route('/Update')
def patch_booking():
    return "Update a booking"