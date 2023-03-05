#!flask/bin/python

import os
import pytest
from flask import json
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

# POST a new booking with valid data
def test_post_valid_booking(app_fixture):

    # Display the message confirming this test is accessed
    app.logger.info("POST a booking with valid data")

    # POST test data
    endpoint_response = app_fixture.post('/booking',
                                         json = {'id': 102934536,
                                                'userId': "21345235",
                                                'createDate': "2023/01/01",
                                                'bookingDate': "2023/01/02",
                                                'bookingTime': "13:15",
                                                'bookingLength': "01:00",
                                                'bookingType': "General use",
                                                'teamEvent': False})

    # Validate that the correct status code was returned
    assert endpoint_response.status_code == 200

    # Decode the returned byte string
    decoded_string = json.loads(endpoint_response.data)

    # Validate that the returned data is correct
    assert decoded_string == {'id': 102934536,
                            'userId': "21345235",
                            'createDate': "2023/01/01",
                            'bookingDate': "2023/01/02",
                            'bookingTime': "13:15",
                            'bookingLength': "01:00",
                            'bookingType': "General use",
                            'teamEvent': False}

    # Inform that the end of this test was reached
    app.logger.info("END OF TEST: test_post_valid_booking")


# POST a new booking with invalid data
def test_post_invalid_booking(app_fixture):

    # Display the message confirming this test is accessed
    app.logger.info("POST a booking with invalid data")

    # POST test data
    endpoint_response = app_fixture.post('/booking',
                                         json = {'id': 1029345362.34324,
                                                'userId': 21345235,
                                                'createDate': "2023/01/01",
                                                'bookingDate': "2023/01/02",
                                                'bookingTime': "13:15",
                                                'bookingLength': "01:00",
                                                'bookingType': "General use",
                                                'teamEvent': False})

    # Validate that the correct error code and message was returned
    assert endpoint_response.status_code == 400

    # Decode the returned byte string
    decoded_string = json.loads(endpoint_response.data)

    # Validate that the returned data is correct
    assert decoded_string == {"IntegrityError": "Invalid data in one or more fields"}

    # Inform that the end of this test was reached
    app.logger.info("END OF TEST: test_post_invalid_booking")


# POST a new booking with missing data
def test_post_missing_booking(app_fixture):

    # Display the message confirming this test is accessed
    app.logger.info("POST a booking with missing data")

    # POST test data
    endpoint_response = app_fixture.post('/booking',
                                         json = {})

    # Validate that the correct error code and message was returned
    assert endpoint_response.status_code == 400

    # Decode the returned byte string
    decoded_string = json.loads(endpoint_response.data)

    # Validate that the returned data is correct
    assert decoded_string == {"KeyError": "Missing data in the request"}

    # Inform that the end of this test was reached
    app.logger.info("END OF TEST: test_post_missing_booking")

# DELETE a booking with valid booking ID
def test_delete_valid_booking(app_fixture):

    # Display the message confirming this test is accessed
    app.logger.info("DELETE a booking with a valid user ID")

    # POST test data
    test_record = app_fixture.post('/booking',
                                    json = {'id': 102934536,
                                            'userId': "21345235",
                                            'createDate': "2023/01/01",
                                            'bookingDate': "2023/01/02",
                                            'bookingTime': "13:15",
                                            'bookingLength': "01:00",
                                            'bookingType': "General use",
                                            'teamEvent': False})

    # Attempt to DELETE data
    endpoint_response = app_fixture.delete("/bookings/102934536")

    # Validate that the correct status code was returned
    assert endpoint_response.status_code == 200

    # Decode the returned byte string
    decoded_string = json.loads(endpoint_response.data)

    # Validate that the returned data is correct
    assert decoded_string == {'id': 102934536,
                            'userId': "21345235",
                            'createDate': "2023/01/01",
                            'bookingDate': "2023/01/02",
                            'bookingTime': "13:15",
                            'bookingLength': "01:00",
                            'bookingType': "General use",
                            'teamEvent': False}

    # Inform that the end of this test was reached
    app.logger.info("END OF TEST: test_delete_valid_booking")

# DELETE a booking with invalid booking ID
def test_delete_missing_booking(app_fixture):

    # Display the message confirming this test is accessed
    app.logger.info("DELETE a booking with an invalid user ID")

    # POST test data
    test_record = app_fixture.post('/booking',
                                    json = {'id': 102934536,
                                            'userId': "21345235",
                                            'createDate': "2023/01/01",
                                            'bookingDate': "2023/01/02",
                                            'bookingTime': "13:15",
                                            'bookingLength': "01:00",
                                            'bookingType': "General use",
                                            'teamEvent': False})

    # Attempt to DELETE data
    endpoint_response = app_fixture.delete("/bookings/100")
    app.logger.error(endpoint_response)


    # Validate that the correct error code and message was returned
    assert endpoint_response.status_code == 400

    # Decode the returned byte string
    decoded_string = json.loads(endpoint_response.data)

    # Validate that the returned data is correct
    assert decoded_string == {"UnmappedInstanceError": "Record not found in the database"}

    # Inform that the end of this test was reached
    app.logger.info("END OF TEST: test_delete_missing_booking")

# GET all bookings of a user by a valid user ID
def test_get_bookings_valid_uid(app_fixture):

    # Display the message confirming this test is accessed
    app.logger.info("GET all bookings of a user by a valid user ID")

    # POST first booking
    test_record_1 = app_fixture.post('/booking',
                                    json = {'id': 102934536,
                                            'userId': "21345235",
                                            'createDate': "2023/01/01",
                                            'bookingDate': "2023/01/02",
                                            'bookingTime': "13:15",
                                            'bookingLength': "01:00",
                                            'bookingType': "General use",
                                            'teamEvent': False})

    # POST second booking
    test_record = app_fixture.post('/booking',
                                    json = {'id': 203948562,
                                            'userId': "21345235",
                                            'createDate': "2023/01/01",
                                            'bookingDate': "2023/01/03",
                                            'bookingTime': "14:30",
                                            'bookingLength': "01:15",
                                            'bookingType': "General use",
                                            'teamEvent': False})

    # Attempt to GET the bookings
    endpoint_response = app_fixture.get("/bookings/user/21345235")

    # Validate that the correct status code was returned
    assert endpoint_response.status_code == 200

    # Decode the returned byte string
    decoded_string = json.loads(endpoint_response.data)

    # Validate that the returned data is correct
    assert decoded_string == [{'id': 102934536,
                               'userId': '21345235',
                               'createDate': '2023/01/01',
                               'bookingDate': '2023/01/02',
                               'bookingTime': '13:15',
                               'bookingLength': '01:00',
                               'bookingType': 'General use',
                               'teamEvent': False},
                              {'id': 203948562,
                               'userId': '21345235',
                               'createDate': '2023/01/01',
                               'bookingDate': '2023/01/03',
                               'bookingTime': '14:30',
                               'bookingLength': '01:15',
                               'bookingType': 'General use',
                               'teamEvent': False}]

    # Inform that the end of this test was reached
    app.logger.info("END OF TEST: test_get_bookings_valid_uid")


# GET all bookings of a user by an invalid user ID
def test_get_bookings_invalid_uid(app_fixture):

    # Display the message confirming this test is accessed
    app.logger.info("GET all bookings of a user by an invalid user ID")

    # POST a test booking
    test_record = app_fixture.post('/booking',
                                    json = {'id': 102934536,
                                            'userId': "21345235",
                                            'createDate': "2023/01/01",
                                            'bookingDate': "2023/01/02",
                                            'bookingTime': "13:15",
                                            'bookingLength': "01:00",
                                            'bookingType': "General use",
                                            'teamEvent': False})

    # Attempt to GET the booking by and invalid user ID
    endpoint_response = app_fixture.get("/bookings/user/222")

    # Validate that the correct status code was returned
    assert endpoint_response.status_code == 200

    # Decode the returned byte string
    decoded_string = json.loads(endpoint_response.data)

    # Validate that an empty list was returned
    assert decoded_string == []

    # Inform that the end of this test was reached
    app.logger.info("END OF TEST: test_get_bookings_invalid_uid")


# GET a specific booking by a valid booking ID
def test_get_booking_valid_bid(app_fixture):

    # Display the message confirming this test is accessed
    app.logger.info("GET a booking by a valid booking ID")

    # POST a test booking
    test_record = app_fixture.post('/booking',
                                    json = {'id': 102934536,
                                            'userId': "21345235",
                                            'createDate': "2023/01/01",
                                            'bookingDate': "2023/01/02",
                                            'bookingTime': "13:15",
                                            'bookingLength': "01:00",
                                            'bookingType': "General use",
                                            'teamEvent': False})

    # Attempt to GET the booking
    endpoint_response = app_fixture.get("/bookings/102934536")

    # Validate that the correct status code was returned
    assert endpoint_response.status_code == 200

    # Decode the returned byte string
    decoded_string = json.loads(endpoint_response.data)

    # Validate that the returned data is correct
    assert decoded_string == {'id': 102934536,
                              'userId': '21345235',
                              'createDate': '2023/01/01',
                              'bookingDate': '2023/01/02',
                              'bookingTime': '13:15',
                              'bookingLength': '01:00',
                              'bookingType': 'General use',
                              'teamEvent': False}

    # Inform that the end of this test was reached
    app.logger.info("END OF TEST: test_get_booking_valid_bid")

# GET a specific booking by an invalid booking ID
def test_get_booking_invalid_bid(app_fixture):

    # Display the message confirming this test is accessed
    app.logger.info("GET a booking by an invalid booking ID")

    # POST a test booking
    test_record = app_fixture.post('/booking',
                                    json = {'id': 102934536,
                                            'userId': "21345235",
                                            'createDate': "2023/01/01",
                                            'bookingDate': "2023/01/02",
                                            'bookingTime': "13:15",
                                            'bookingLength': "01:00",
                                            'bookingType': "General use",
                                            'teamEvent': False})

    # Attempt to GET the booking by and invalid user ID
    endpoint_response = app_fixture.get("/bookings/222")

    # Validate that the correct status code was returned
    assert endpoint_response.status_code == 400

    # Decode the returned byte string
    decoded_string = json.loads(endpoint_response.data)

    # Validate that the returned data is correct
    assert decoded_string == {"AttributeError": "The referenced record does not exist"}

    # Inform that the end of this test was reached
    app.logger.info("END OF TEST: test_get_booking_invalid_bid")

# PATCH a booking with valid data
def test_patch_valid_booking(app_fixture):

    # Display the message confirming this test is accessed
    app.logger.info("PATCH a booking by a valid booking ID")

    # POST a test booking
    test_record = app_fixture.post('/booking',
                                    json = {'id': 102934536,
                                            'userId': "21345235",
                                            'createDate': "2023/01/01",
                                            'bookingDate': "2023/01/02",
                                            'bookingTime': "13:15",
                                            'bookingLength': "01:00",
                                            'bookingType': "General use",
                                            'teamEvent': False})

    # Decode the returned byte string
    decoded_string = json.loads(test_record.data)

    # Display the record after POST
    app.logger.info(f"POSTed test data: {decoded_string}")

    # PATCH the booking time and length
    update_record = app_fixture.patch('/bookings/102934536',
                                      json = {'bookingTime': "14:15",
                                              'bookingLength': "01:30",
                                             })

    # Decode the returned byte string
    decoded_string = json.loads(update_record.data)

    # Display the record after PATCH
    app.logger.info(f"PATCHed test data: {decoded_string}")

    # Validate that the correct status code was returned
    assert update_record.status_code == 200

    # Decode the returned byte string
    decoded_string = json.loads(update_record.data)

    # Validate that the returned data is correctly updated
    assert decoded_string == {'id': 102934536,
                              'userId': "21345235",
                              'createDate': "2023/01/01",
                              'bookingDate': "2023/01/02",
                              'bookingTime': "14:15",
                              'bookingLength': "01:30",
                              'bookingType': "General use",
                              'teamEvent': False}

    # Inform that the end of this test was reached
    app.logger.info("END OF TEST: test_patch_valid_booking")

# PATCH a booking with invalid data
def test_patch_invalid_booking(app_fixture):

    # Display the message confirming this test is accessed
    app.logger.info("PATCH a booking using invalid data type in bookingTime")

    # POST a test booking
    test_record = app_fixture.post('/booking',
                                    json = {'id': 102934536,
                                            'userId': "21345235",
                                            'createDate': "2023/01/01",
                                            'bookingDate': "2023/01/02",
                                            'bookingTime': "13:15",
                                            'bookingLength': "01:00",
                                            'bookingType': "General use",
                                            'teamEvent': False})

    # Decode the returned byte string
    decoded_string = json.loads(test_record.data)

    # PATCH the booking time and length using invalid data type
    update_record = app_fixture.patch('/bookings/102934536',
                                      json = {'bookingTime': 235234523,
                                              'bookingLength': "01:30",
                                             })

    # Decode the returned byte string
    decoded_string = json.loads(update_record.data)

    # Validate that the correct error code and message was returned
    assert update_record.status_code == 400

    # Validate that the returned data is correct
    assert decoded_string == {"TypeError": "Endpoint function operating on a wrong data type"}

    # Inform that the end of this test was reached
    app.logger.info("END OF TEST: test_patch_invalid_booking")

# PATCH a booking with missing data
def test_patch_missing_booking(app_fixture):

    # Display the message confirming this test is accessed
    app.logger.info("PATCH a non-existent booking")

    # PATCH the booking time and length of a non-existent booking
    update_record = app_fixture.patch('/bookings/102',
                                      json = {'bookingTime': 235234523,
                                              'bookingLength': "01:30",
                                             })

    # Decode the returned byte string
    decoded_string = json.loads(update_record.data)

    # Validate that the correct error code and message was returned
    assert update_record.status_code == 400

    # Validate that the returned data is correct
    assert decoded_string == {"AttributeError": "The referenced record does not exist"}

    # Inform that the end of this test was reached
    app.logger.info("END OF TEST: test_patch_missing_booking")
