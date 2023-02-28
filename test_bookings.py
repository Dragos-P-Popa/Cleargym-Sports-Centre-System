#!flask/bin/python

import os
import pytest
from flask import json, request, Flask
from flask_sqlalchemy import SQLAlchemy
from app import app, db, models
# from app.models import
from flask_login import current_user, login_user, logout_user

# The function responsible for setting up and tearing down all the data
# and objects that may be reused in multiple tests
@pytest.fixture
def app_fixture():

    app.logger.info("Start of the 'set up' / 'tear down' function")

    app.config.from_object('config')
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    # Setting up temporary database tables in memory
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    # Create the tables
    db.create_all()

    # 'yield' returns the app's test instance to whatever function
    # makes use of this fixture
    yield app.test_client()

    # Delete the tables
    db.drop_all()

    app.logger.info("End of the 'set up' / 'tear down' function")

# Show the app instance returned by the app_fixture() function
def test_fixture_setup(app_fixture):
    app.logger.info(f"The app_fixture() function returns {app_fixture}")
    assert True

# POST a new booking with valid data
def test_post_valid_booking(app_fixture):

    # Display the message confirming this test is accessed
    app.logger.info("POST a booking with valid data")

    # POST test data
    endpoint_response = app_fixture.post('/booking',
                                         json = {"id" : 102934536,
                                                 "userId" : "21345235"})

    # Validate that the correct error code and message was returned
    assert endpoint_response.status_code == 200

    # Decode the returned byte string
    decoded_string = json.loads(endpoint_response.data)

    # Validate that the returned data is correct
    assert decoded_string == {"id" : 102934536, "userId" : "21345235"}

    # Inform that the end of this test was reached
    app.logger.info("END OF TEST: test_post_valid_booking")

# POST a new booking with invalid data
def test_post_invalid_booking(app_fixture):

    # Display the message confirming this test is accessed
    app.logger.info("POST a booking")

    # POST test data
    endpoint_response = app_fixture.post('/booking',
                                         json = {"id" : 102.92,
                                                 "userId" : "21345235"})

    # Validate that the correct error code and message was returned
    assert endpoint_response.status_code == 200

    # Decode the returned byte string
    decoded_string = json.loads(endpoint_response.data)

    # Validate that the returned data is correct
    assert decoded_string == {"id" : 102.92, "userId" : "21345235"}

    # Display the data of the response
    app.logger.info(f"The endpoint response data: {endpoint_response.data}")

    # Inform that the end of this test was reached
    app.logger.info("END OF TEST: test_post_invalid_booking")