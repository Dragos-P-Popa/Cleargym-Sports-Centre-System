from app import app , db , models
from flask import render_template, flash, request, redirect,jsonify
import logging

# The route corresponding to retrieving, updating and deleting a booking
# by its ID
@app.route('/bookings/{id}', methods=['GET', 'PATCH', 'DELETE'])
def get_patch_del_booking(id):

    # Validate which request was made and execute the corresponding code

    if bool(request.method == 'GET'):
        # Logger used for debugging through more informative console messages
        app.logger.info('A request to GET a booking by its ID')

        booking = models.TRY.query.get(id)

        if not booking:
                return jsonify({'message': 'Missing fields'}), 400
        
        db.session.commit()
        response = {'id': booking.id, 
                'userId': booking.userId}

        return {'booking': response}, 200


    if bool(request.method == 'PATCH'): # & (form.validate_on_submit()) once we have forms
        app.logger.info('A request to PATCH a booking by its ID')
        return "Updating a booking by its ID"

    if bool(request.method == 'DELETE'):

        app.logger.info('A request to DELETE a booking by its ID')

        booking = models.TRY.query.get(id)

        if not booking:
            return jsonify({'message': 'Missing fields'}), 400
        
        db.session.delete(booking)
        db.session.commit()

        return '',204
        #print( "Deleting a booking by its ID")

# The route corresponding to retrieving a booking by the user's ID
@app.route('/bookings/user/{userId}', methods=['GET'])
def get_booking_by_uid(userId):
    # Validate that a correct request was sent to this API
    if bool(request.method == 'GET'):

        app.logger.info('A request to GET a booking by the user\'s ID')

        booking = models.TRY.query.filter_by(userId=userId).first()

        if not booking:
            return jsonify({'message': 'Missing fields'}), 400
        
        db.session.commit()

        response = {'id': booking.id, 
                'userId': booking.userId}

        return {'booking': response}, 200
       

# The route corresponding to creating a new booking
@app.route('/booking', methods=['POST'])
def post_booking():
    # Validate that a correct request was sent to this API
    if bool(request.method == 'POST'): # & (form.validate_on_submit()) once we have forms

        app.logger.info('A request to GET a booking by the user\'s ID')

        Info = request.get_json()

        if not Info:
            return jsonify({'message': 'Missing fields'}), 400

        booking = models.TRY(
            id=Info["id"],
            userId=Info["userId"]
            )

        db.session.add(booking)
        db.session.commit()

        response = {'id': booking.id, 
                    'userId': booking.userId}

        return {'booking': response}, 200
