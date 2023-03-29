#!flask/bin/python

from flask import json
from app import app, db


######################## ACTIVITY TABLE ENDPOINTS TESTS ########################

# The function responsible for adding a temporary record to the Facility table
def add_facility(fixture):
    
    # POST test data
    endpoint_response = fixture.post('/facility', json={
        'facilityName': "Gym",
        'capacity': 30,
        'openingTime': "08:00:00",
        'closingTime': "20:00:00",
        'managerId': "63F0DE4724EF6726E1F27D57"})

    return

# POST a new activity with valid data
def test_post_valid_activity(app_fixture):

    # Display the message confirming this test is accessed
    app.logger.info("POST an activity with valid data")

    # Create an activity related to this booking
    add_facility(app_fixture)

    # POST test data
    endpoint_response = app_fixture.post('/activity',
                                         json = {'activityType': 'General use',
                                                 'activityStartTime': "17:00",
                                                 'activityEndTime': "18:00",
                                                 'activityDay': 'Monday',
                                                 'price': 10.0,
                                                 'productId': 1,
                                                 'facilityId': 1})

    # Validate that the correct status code was returned
    assert endpoint_response.status_code == 200

    # Decode the returned byte string
    decoded_string = json.loads(endpoint_response.data)

    # Validate that the returned data is correct
    assert decoded_string == {'activityId': 11,
                              'activityType': 'General use',
                              'activityStartTime': "17:00",
                              'activityEndTime': "18:00",
                              'activityDay': 'Monday',
                              'price': 10.0,
                              'productId': 1,}

    # Inform that the end of this test was reached
    app.logger.info("END OF TEST: test_post_valid_activity")


# POST a new activity with invalid 'activityStartTime' format
def test_post_invalid_activity(app_fixture):

    # Display the message confirming this test is accessed
    app.logger.info("POST an activity with invalid data")

    # Create an activity related to this booking
    add_facility(app_fixture)

    # POST test data
    endpoint_response = app_fixture.post('/activity',
                                         json = {'activityType': 'General use',
                                                 'activityStartTime': "abcdef",
                                                 'activityEndTime': "18:00",
                                                 'activityDay': 'Monday',
                                                 'price': 10.0,
                                                 'productId': 1,
                                                 'facilityId': 1})

    # Validate that the correct error code and message was returned
    assert endpoint_response.status_code == 400

    # Decode the returned byte string
    decoded_string = json.loads(endpoint_response.data)

    # Validate that the returned data is correct
    assert decoded_string == {"ValueError": "Data does not match the required" +
                                            " format in one or more fields"}

    # Inform that the end of this test was reached
    app.logger.info("END OF TEST: test_post_invalid_activity")


# POST a new activity with missing data
def test_post_missing_activity(app_fixture):

    # Display the message confirming this test is accessed
    app.logger.info("POST an activity with missing data")

    # Create an activity related to this booking
    add_facility(app_fixture)

    # POST test data
    endpoint_response = app_fixture.post('/activity',
                                         json = {})

    # Validate that the correct error code and message was returned
    assert endpoint_response.status_code == 400

    # Decode the returned byte string
    decoded_string = json.loads(endpoint_response.data)

    # Validate that the returned data is correct
    assert decoded_string == {"KeyError": "Missing data in the request"}

    # Inform that the end of this test was reached
    app.logger.info("END OF TEST: test_post_missing_activity")


# DELETE an activity with a valid activity ID
def test_delete_valid_activity(app_fixture):

    # Display the message confirming this test is accessed
    app.logger.info("DELETE an activity with a valid activity ID")

    # Create an activity related to this booking
    add_facility(app_fixture)

    # POST test data
    test_record = app_fixture.post('/activity',
                                    json = {'activityType': 'General use',
                                            'activityStartTime': "17:00",
                                            'activityEndTime': "18:00",
                                            'activityDay': 'Monday',
                                            'price': 10.0,
                                            'productId': 1,
                                            'facilityId': 1})

    # Attempt to DELETE data
    endpoint_response = app_fixture.delete("/activity/1")

    # Validate that the correct status code was returned
    assert endpoint_response.status_code == 200

    # Decode the returned byte string
    decoded_string = json.loads(endpoint_response.data)

    # Validate that the returned data is correct
    assert decoded_string == {'activityId': 1,
                              'activityType': 'General use',
                              'activityStartTime': "17:00",
                              'activityEndTime': "18:00",
                              'activityDay': 'Monday',
                              'price': 10.0,
                              'productId': 1}

    # Inform that the end of this test was reached
    app.logger.info("END OF TEST: test_delete_valid_activity")


# DELETE an activity with an invalid activity ID
def test_delete_missing_activity(app_fixture):

    # Display the message confirming this test is accessed
    app.logger.info("DELETE an activity with an invalid activity ID")

    # Create an activity related to this booking
    add_facility(app_fixture)

    # POST test data
    test_record = app_fixture.post('/activity',
                                    json = {'activityType': 'General use',
                                            'activityStartTime': "17:00",
                                            'activityEndTime': "18:00",
                                            'activityDay': 'Monday',
                                            'price': 10.0,
                                            'productId': 1,
                                            'facilityId': 1})

    # Attempt to DELETE data
    endpoint_response = app_fixture.delete("/activity/100")
    app.logger.error(endpoint_response)

    # Validate that the correct error code and message was returned
    assert endpoint_response.status_code == 400

    # Decode the returned byte string
    decoded_string = json.loads(endpoint_response.data)

    # Validate that the returned data is correct
    assert decoded_string == {"UnmappedInstanceError": "Record not found in the database"}

    # Inform that the end of this test was reached
    app.logger.info("END OF TEST: test_delete_missing_activity")


# GET a specific activity by a valid activity ID
def test_get_activity_valid_id(app_fixture):

    # Display the message confirming this test is accessed
    app.logger.info("GET an activity by a valid activity ID")

    # Create an activity related to this booking
    add_facility(app_fixture)

    # POST test data
    test_record = app_fixture.post('/activity',
                                    json = {'activityType': 'General use',
                                            'activityStartTime': "17:00",
                                            'activityEndTime': "18:00",
                                            'activityDay': 'Monday',
                                            'price': 10.0,
                                            'productId': 1,
                                            'facilityId': 1})

    # Attempt to GET the activity
    endpoint_response = app_fixture.get("/activity/1")

    # Validate that the correct status code was returned
    assert endpoint_response.status_code == 200

    # Decode the returned byte string
    decoded_string = json.loads(endpoint_response.data)

    # Validate that the returned data is correct
    assert decoded_string == {'activityId': 1,
                              'activityType': 'General use',
                              'activityStartTime': "17:00",
                              'activityEndTime': "18:00",
                              'activityDay': 'Monday',
                              'price': 10.0,
                              'productId': 1}

    # Inform that the end of this test was reached
    app.logger.info("END OF TEST: test_get_activity_valid_id")


# GET a specific activity by an invalid activity ID
def test_get_activity_invalid_id(app_fixture):

    # Display the message confirming this test is accessed
    app.logger.info("GET an activity by an invalid activity ID")

    # Create an activity related to this booking
    add_facility(app_fixture)

    # POST test data
    test_record = app_fixture.post('/activity',
                                    json = {'activityType': 'General use',
                                            'activityStartTime': "17:00",
                                            'activityEndTime': "18:00",
                                            'activityDay': 'Monday',
                                            'price': 10.0,
                                            'productId': 1,
                                            'facilityId': 1})

    # Attempt to GET the activity by and invalid activity ID
    endpoint_response = app_fixture.get("/activity/222")

    # Validate that the correct status code was returned
    assert endpoint_response.status_code == 400

    # Decode the returned byte string
    decoded_string = json.loads(endpoint_response.data)

    # Validate that the returned data is correct
    assert decoded_string == {"AttributeError": "The referenced record does not exist"}

    # Inform that the end of this test was reached
    app.logger.info("END OF TEST: test_get_activity_invalid_id")


# PATCH a activity with valid data
def test_patch_valid_activity(app_fixture):

    # Display the message confirming this test is accessed
    app.logger.info("PATCH an activity by a valid activity ID")

    # Create an activity related to this booking
    add_facility(app_fixture)

    # POST test data
    test_record = app_fixture.post('/activity',
                                    json = {'activityType': 'General use',
                                            'activityStartTime': "17:00",
                                            'activityEndTime': "18:00",
                                            'activityDay': 'Monday',
                                            'price': 10.0,
                                            'productId': 1,
                                            'facilityId': 1})

    # Decode the returned byte string
    decoded_string = json.loads(test_record.data)

    # Display the record after POST
    app.logger.info(f"POSTed test data: {decoded_string}")

    # PATCH the activity start time and day
    update_record = app_fixture.patch('/activity/1',
                                      json = {'activityStartTime': "14:00",
                                              'activityDay': "Tuesday",
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
    assert decoded_string == {'activityId': 1,
                              'activityType': "General use",
                              'activityStartTime': "14:00",
                              'activityEndTime': "18:00",
                              'activityDay': "Tuesday",
                              'price': 10.0,
                              'productId': 1}

    # Inform that the end of this test was reached
    app.logger.info("END OF TEST: test_patch_valid_activity")


# PATCH an activity with invalid data
def test_patch_invalid_activity(app_fixture):

    # Display the message confirming this test is accessed
    app.logger.info("PATCH an activity using invalid data type in activityStartTime")

    # Create an activity related to this booking
    add_facility(app_fixture)

    # POST test data
    test_record = app_fixture.post('/activity',
                                    json = {'activityType': 'General use',
                                            'activityStartTime': "17:00",
                                            'activityEndTime': "18:00",
                                            'activityDay': 'Monday',
                                            'price': 10.0,
                                            'productId': 1,
                                            'facilityId': 1})

    # Decode the returned byte string
    decoded_string = json.loads(test_record.data)

    # PATCH the booking time and length using invalid data type
    update_record = app_fixture.patch('/activity/1',
                                      json = {'activityStartTime': 235234523})

    # Decode the returned byte string
    decoded_string = json.loads(update_record.data)

    # Validate that the correct error code and message was returned
    assert update_record.status_code == 400

    # Validate that the returned data is correct
    assert decoded_string == {"TypeError": "Endpoint function operating on a wrong data type"}

    # Inform that the end of this test was reached
    app.logger.info("END OF TEST: test_patch_invalid_activity")


# PATCH an activity with missing data
def test_patch_missing_activity(app_fixture):

    # Display the message confirming this test is accessed
    app.logger.info("PATCH a non-existent activity")

    # Create an activity related to this booking
    add_facility(app_fixture)

    # PATCH the activityStartTime value of a non-existent activity
    update_record = app_fixture.patch('/activity/101',
                                      json = {'activityStartTime': "14:00"})

    # Decode the returned byte string
    decoded_string = json.loads(update_record.data)

    # Validate that the correct error code and message was returned
    assert update_record.status_code == 400

    # Validate that the returned data is correct
    assert decoded_string == {"AttributeError": "The referenced record does not exist"}

    # Inform that the end of this test was reached
    app.logger.info("END OF TEST: test_patch_missing_activity")
