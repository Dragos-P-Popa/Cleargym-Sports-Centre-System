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

    print("Testing the 'set up' / 'tear down' function")

    app.config.from_object('config')
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    # Absolute path to config file's directory
    #basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    # Create the database
    db.create_all()

    # 'yield' returns the app instance to whatever function makes use of this fixture
    yield app.test_client()

    db.drop_all()

    print("End of the 'set up' / 'tear down' function")

# A temporary placeholder function for testing the set up and teardown
# It should always return True
def test_placeholder0(app_fixture):
    app.logger.info(f"The creation of {app_fixture} was successful")
    app.logger.info('asserting True')
    assert True

# A temporary placeholder function for testing the output when 'False' is returned
# def test_placeholder1():
    # app.logger.error('asserting False')
    # assert False


####### WORK IN PROGRESS #######


# Testing if an app instance can successfully POST new bookings
def test_post_booking(app_fixture):

    # Display the message confirming this test is accessed
    app.logger.info("POST a booking")

    # POST test data
    endpoint_response = app_fixture.post('/booking',
                                         json = {"id" : "102934536",
                                                 "userId" : "21345235"})

    # Validate that the correct error code and message was returned
    assert endpoint_response.status_code == 200

    # Decode the returned byte string
    decoded_string = json.loads(endpoint_response.data)

    # Validate that the returned data is correct
    assert decoded_string == {"id" : "102934536", "userId" : "21345235"}

    # Display the data of the response
    app.logger.info(f"The endpoint response data: {endpoint_response.data}")

    # Inform of a successful test
    app.logger.info("SUCCESSFUL TEST: test_post_booking")
