#!flask/bin/python

import os
import pytest
from flask import Flask
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
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'Booking.db')
    self.app = app.test_client()
    db.create_all()

    # 'yield' returns the app instance to whatever function makes use of this fixture
    yield app

    print("End of the 'set up' / 'tear down' function")

# A temporary placeholder function for testing the set up and teardown
# It should always return True
def test_placeholder0(app_fixture):
    app.logger.info(f"Printing the {app_fixture}")
    print(f"Printing the {app_fixture}")
    app.logger.info('asserting True')
    assert True

# A temporary placeholder function for testing the output when 'False' is returned
def test_placeholder1():
    app.logger.error('asserting False')
    assert False

# Testing the /booking endpoint when trying to POST null data
def post_empty_booking_test(app_fixture):

    # Display the message confirming this test is accessed
    app.logger.info("POST an empty booking")

    # POST a request with no data and assign the response to this variable
    endpoint_response = app_fixture.post('/booking', data = None)

    # Validate that the correct error code and message was returned
    assert endpoint_response.status_code == 400
    assert endpoint_response.json == {'message': 'Missing fields'}




