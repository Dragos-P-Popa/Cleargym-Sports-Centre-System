#!flask/bin/python

import os
import pytest
from flask import json, request, Flask
from app import app, db

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
def test_create_valid_facility(app_fixture):
    app.logger.info("POST a faciliy with valid data")

    #POST test data
    endpoint_response = app_fixture.post('/facility', json ={
        'facilityName': "Gym",
        'capacity': 30,
        'openingTime': "08:00:00",
        'closingTime': "20:00:00",
        'managerId': "63F0DE4724EF6726E1F27D57"})
    
    # Validate that the correct error code and message was returned
    assert endpoint_response.status_code == 200

    # Decode the returned byte string
    decoded_string = json.loads(endpoint_response.data)
    del decoded_string['id']  # id is randomly generated

    # Validate that the returned data is correct
    assert decoded_string == {
        'facilityName': "Gym",
        'capacity': 30,
        'openingTime': "08:00:00",
        'closingTime': "20:00:00",
        'managerId': "63F0DE4724EF6726E1F27D57"}
    
    app.logger.info("END OF TEST: test_post_valid_facility")


# GET a facility with valid facility ID
def test_get_validID_facility(app_fixture):

    app.logger.info("GET a facility with valid ID")

    #POST a facility first
    test_record_1 = app_fixture.post('/facility', json ={  
        'facilityName': "Swimming Pool",
        'capacity': 30,
        'openingTime': "08:00:00",
        'closingTime': "20:00:00",
        'managerId': "63F0DE4724EF6726E1F27D57"})

    #POST a second facility
    test_record_2 = app_fixture.post('/facility', json={
        'facilityName': "Tennis court",
        'capacity': 4,
        'openingTime': "08:00:00",
        'closingTime': "20:00:00",
        'managerId': "24F01E5793QF9716E1F29E57"})
    
    decoded_string = json.loads(test_record_1.data)
    testId = decoded_string['id']
    
    #Attempt to get the facilitt
    endpoint_response = app_fixture.get(f"/facility/{testId}")
    assert endpoint_response.status_code == 200

    # Decode the returned byte string
    decoded_string = json.loads(endpoint_response.data)
    assert decoded_string == {
        'id': testId,
        'facilityName': "Swimming Pool",
        'capacity': 30,
        'openingTime': "08:00:00",
        'closingTime': "20:00:00",
        'managerId': "63F0DE4724EF6726E1F27D57"}
    
    app.logger.info("END OF TEST: test_get_validID_facility")

    
# GET a facility with a Valid Facility Name
def test_get_validName_facility(app_fixture):

    app.logger.info("GET a facility with valid name")

    #POST a facility first
    test_record_1 = app_fixture.post('/facility', json ={  
        'facilityName': "Swimming Pool",
        'capacity': 30,
        'openingTime': "08:00:00",
        'closingTime': "20:00:00",
        'managerId': "63F0DE4724EF6726E1F27D57"})

    #POST a second facility
    test_record_2 = app_fixture.post('/facility', json ={  
        'facilityName': "Tennis court 1",
        'capacity': 4,
        'openingTime': "08:00:00",
        'closingTime': "20:00:00",
        'managerId': "24F01E5793QF9716E1F29E57"})
    
    #Attempt to get the facilitt
    endpoint_response = app_fixture.get("/facility/Tennis court 1")
    assert endpoint_response.status_code == 200

    # Decode the returned byte string
    decoded_string = json.loads(endpoint_response.data)
    del decoded_string['id']
    assert decoded_string == {
        'facilityName': "Tennis court 1",
        'capacity': 4,
        'openingTime': "08:00:00",
        'closingTime': "20:00:00",
        'managerId': "24F01E5793QF9716E1F29E57"}
    
    app.logger.info("END OF TEST: test_get_validName_facility")
    
# PATCH a valid facility
def test_valid_patch_facility(app_fixture):
    app.logger.info("GET a facility with valid name")

    test_record_1 = app_fixture.post('/facility', json={
        'facilityName': "Swimming Pool",
        'capacity': 30,
        'openingTime': "08:00:00",
        'closingTime': "20:00:00",
        'managerId': "63F0DE4724EF6726E1F27D57"})

    test_record_2 = app_fixture.post('/facility', json={
        'facilityName': "Tennis court 1",
        'capacity': 4,
        'openingTime': "08:00:00",
        'closingTime': "20:00:00",
        'managerId': "24F01E5793QF9716E1F29E57"})

    update_record = app_fixture.patch('facility/Swimming Pool', json={
        'capacity': 20,
        'openingTime': "09:00:00"})

    decoded_string = json.loads(update_record.data)
    assert update_record.status_code == 200
    del decoded_string['id']

    assert decoded_string == {
        'facilityName': "Swimming Pool",
        'capacity': 20,
        'openingTime': "09:00:00",
        'closingTime': "20:00:00",
        'managerId': "63F0DE4724EF6726E1F27D57"}
    
    app.logger.info("END OF TEST: test_valid_patch_facility")

  

