#!flask/bin/python

import os
import pytest
from flask import json, request, Flask
from flask_sqlalchemy import SQLAlchemy
from app import app, db, models

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

#testing to add a new facility with valid data
def test_create_facility_with_valid_data(app_fixture):
    app.logger.info("POST a faciliy with valid data")

    #POST test data
    endpoint_response = app_fixture.post('/facility', json = {  'id': 102934536,
                                                                'facilityName': "Swimming Pool",
                                                                'capacity': 30,
                                                                'openingTime': "8:00:00",
                                                                'closingTime': "20:00:00",
                                                                'managerID': "63F0DE4724EF6726E1F27D57"})
    
    # Validate that the correct error code and message was returned
    assert endpoint_response.status_code == 200

    # Decode the returned byte string
    decoded_string = json.loads(endpoint_response.data)

    # Validate that the returned data is correct
    assert decoded_string == {'id': 102934536,
                              'facilityName': "Swimming Pool",
                              'capacity': 30,
                              'openingTime': "8:00:00",
                              'closingTime': "20:00:00",
                              'managerID': "63F0DE4724EF6726E1F27D57"}
    
    app.logger.info("END OF TEST: test_post_valid_facility")


#testing to add a new facility with invalid data
def test_post_invalid_facility(app_fixture):

    # Display the message confirming this test is accessed
    app.logger.info("POST a facility with invalid data")

    # POST test data
    endpoint_response = app_fixture.post('/facility', json = {  'id': 102934536,
                                                                'facilityName': "Swimming Pool",
                                                                'capacity': "30ABC",
                                                                'openingTime': "8:A0:00",
                                                                'closingTime': "20:0B:00",
                                                                'managerID': "63F0DE4724EF6726E1F27D57"})

    # Validate that the correct error code and message was returned
    assert endpoint_response.status_code == 400

    # Decode the returned byte string
    decoded_string = json.loads(endpoint_response.data)

    # Validate that the returned data is correct
    #assert decoded_string == {"Error": "Invalid or missing data in one or more fields"} --------------

    # Inform that the end of this test was reached
    app.logger.info("END OF TEST: test_post_invalid_facility")

# POST a new booking with missing data
def test_post_missing_facility(app_fixture):

    # Display the message confirming this test is accessed
    app.logger.info("POST a facility with missing data")

    # POST test data
    endpoint_response = app_fixture.post('/booking',
                                         json = {})

    # Validate that the correct error code and message was returned
    assert endpoint_response.status_code == 400

    # Decode the returned byte string
    decoded_string = json.loads(endpoint_response.data)

    # Validate that the returned data is correct
    # assert decoded_string == {"Error": "No data in the request"} ------------------

    # Inform that the end of this test was reached
    app.logger.info("END OF TEST: test_post_missing_booking")

# GET a facility with valid facility ID
def test_get_validID_facility(app_fixture):

    app.logger.info("GET a facility with valid ID")

    #POST a facility first
    test_record_1 = app_fixture.post('/facility', json = {  'id': 102934536,
                                                            'facilityName': "Swimming Pool",
                                                            'capacity': 30,
                                                            'openingTime': "8:00:00",
                                                            'closingTime': "20:00:00",
                                                            'managerID': "63F0DE4724EF6726E1F27D57"})

    #POST a second facility
    test_record_1 = app_fixture.post('/facility', json = {  'id': 123456789,
                                                            'facilityName': "Tennis court",
                                                            'capacity': 4,
                                                            'openingTime': "8:00:00",
                                                            'closingTime': "20:00:00",
                                                            'managerID': "24F01E5793QF9716E1F29E57"})
    
    #Attempt to get the facilitt
    endpoint_response = app_fixture.get("/bookings/id/102944536")
    assert endpoint_response.status_code == 200

    # Decode the returned byte string
    decoded_string = json.loads(endpoint_response.data)
    assert decoded_string == {'id': 102934536,
                              'facilityName': "Swimming Pool",
                              'capacity': 30,
                              'openingTime': "8:00:00",
                              'closingTime': "20:00:00",
                              'managerID': "63F0DE4724EF6726E1F27D57"}
    
    app.logger.info("END OF TEST: test_get_validID_facility")

# GET a facility with a Valid Facility Name
def test_get_validName_facility(app_fixture):

    app.logger.info("GET a facility with valid name")

    #POST a facility first
    test_record_1 = app_fixture.post('/facility', json = {  'id': 102934536,
                                                            'facilityName': "Swimming Pool",
                                                            'capacity': 30,
                                                            'openingTime': "8:00:00",
                                                            'closingTime': "20:00:00",
                                                            'managerID': "63F0DE4724EF6726E1F27D57"})

    #POST a second facility
    test_record_1 = app_fixture.post('/facility', json = {  'id': 123456789,
                                                            'facilityName': "Tennis court 1",
                                                            'capacity': 4,
                                                            'openingTime': "8:00:00",
                                                            'closingTime': "20:00:00",
                                                            'managerID': "24F01E5793QF9716E1F29E57"})
    
    #Attempt to get the facilitt
    endpoint_response = app_fixture.get("/bookings/facilityName/Tennis court")
    assert endpoint_response.status_code == 200

    # Decode the returned byte string
    decoded_string = json.loads(endpoint_response.data)
    assert decoded_string == {  'id': 123456789,
                                'facilityName': "Tennis court 1",
                                'capacity': 4,
                                'openingTime': "8:00:00",
                                'closingTime': "20:00:00",
                                'managerID': "24F01E5793QF9716E1F29E57"}
    
    app.logger.info("END OF TEST: test_get_validName_facility")

#GET facility with invalid data

#PATCH facility
# def test_patch_valid_facility(app_fixture):

#     app.logger.info("PATCH a facility capacity with valid ID")

#     #POST a facility first
#     test_record_1 = app_fixture.post('/facility', json = {  'id': 102934536,
#                                                             'facilityName': "Swimming Pool",
#                                                             'capacity': 30,
#                                                             'openingTime': "8:00:00",
#                                                             'closingTime': "20:00:00",
#                                                             'managerID': "63F0DE4724EF6726E1F27D57"})
