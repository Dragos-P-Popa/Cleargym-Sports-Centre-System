from app import app
from flask import render_template, flash, request, redirect
import logging

# The route corresponding to retrieving, updating and deleting a booking
# by its ID
@app.route('/bookings/{id}', methods=['GET', 'PATCH', 'DELETE'])
def access_bookings():

    # Validate which request was made and execute the corresponding code

    if bool(request.method == 'GET'):
        # Logger used for debugging through more informative console messages
        app.logger.info('A request to GET a booking by its ID')
        # Temporarily returning a string for debugging
        return "Returning a booking by its ID"

    if bool(request.method == 'PATCH'): # & (form.validate_on_submit()) once we have forms
        app.logger.info('A request to PATCH a booking by its ID')
        return "Updating a booking by its ID"

    if bool(request.method == 'DELETE'):
        app.logger.info('A request to DELETE a booking by its ID')
        print( "Deleting a booking by its ID")

# The route corresponding to retrieving a booking by the user's ID
@app.route('/bookings/user/{userId}', methods=['GET'])
def get_by_uid():
    # Validate that a correct request was sent to this API
    if bool(request.method == 'GET'):
        app.logger.info('A request to GET a booking by the user\'s ID')
        return "Returning a booking by the user\'s ID"

# The route corresponding to creating a new booking
@app.route('/booking', methods=['POST'])
def create():
    # Validate that a correct request was sent to this API
    if bool(request.method == 'POST'): # & (form.validate_on_submit()) once we have forms
        app.logger.info('A request to GET a booking by the user\'s ID')
        return "Returning a booking by the user\'s ID"
