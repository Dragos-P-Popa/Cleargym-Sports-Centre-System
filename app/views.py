from app import app, db, models
from flask import request, jsonify, Flask
import datetime
from datetime import datetime, date, time


@app.route('/booking', methods=['POST'])
def post_booking():
    Info = request.get_json()

    if not Info:
        return jsonify({'message': 'Missing fields'}), 400

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

    db.session.add(booking)
    db.session.commit()

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


@app.route('/booking/<int:id>', methods=['DELETE'])
def delete_booking(id):
    booking = models.booking.query.get(id)
    # check for error
    if not booking:
        return jsonify({'message': 'Booking does not exist'}), 400

    db.session.delete(booking)
    db.session.commit()

    response = {'id': booking.id,
                'userId': booking.userId,
                'createDate': booking.createDate.strftime('%y/%m/%d'),
                'bookingDate': booking.bookingDate.strftime('%y/%m/%d'),
                'bookingTime': booking.bookingTime.strftime('%H:%M'),
                'bookingLength': booking.bookingLength.strftime('%H:%M'),
                'bookingType': booking.bookingType,
                'teamEvent': booking.teamEvent
                }

    return {'booking': response}, 200


@app.route('/Update')
def patch_booking():
    return "Update a booking"


@app.route('/bookings/user/<userId>', methods=['GET'])
def get_booking_uid(userId):
    bookings = models.booking.query.filter_by(userId=userId).all()

    if not bookings:
        return jsonify({'message': 'Booking does not exist'}), 400

    db.session.commit()
    if bookings:
        booking_list = []
        for booking in bookings:
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
        return jsonify(booking_list)


@app.route('/bookings/<int:id>', methods=['GET'])
def get_booking_bid(id):
    booking = models.booking.query.get(id)
    # check for error
    if not booking:
        return jsonify({'message': 'Booking does not exist'}), 400

    db.session.commit()

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
