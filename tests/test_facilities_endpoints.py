#!flask/bin/python

import os
import pytest
from flask import json, request, Flask
from app import app, db


######################## FACILITY TABLE ENDPOINTS TESTS ########################


# POST new facility with valid data
def test_post_valid_facility(app_fixture):
    app.logger.info("POST a faciliy with valid data")

    # POST test data
    endpoint_response = app_fixture.post('/facility', json={
        'facilityName': "Gym",
        'capacity': 30,
        'openingTime': "08:00:00",
        'closingTime': "20:00:00",
        'managerId': "63F0DE4724EF6726E1F27D57"})

    # Validate that the correct error code and message was returned
    assert endpoint_response.status_code == 200

    # Decode the returned string
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


# POST facility with wrong data type
def test_post_invalid_format_facility(app_fixture):
    app.logger.info("POST a facility with invalid format data")

    # POST test data
    endpoint_response = app_fixture.post('/facility', json={
        'facilityName': "Gym",
        'capacity': 30,
        'openingTime': "08:A0:00",
        'closingTime': "20:00:00",
        'managerId': "63F0DE4724EF6726E1F27D57"})

    assert endpoint_response.status_code == 400
    decoded_string = json.loads(endpoint_response.data)

    assert decoded_string == {
        'ValueError': 'Data does not match the required format in one or more fields'}

    app.logger.info("END OF TEST: test_post_invalid_facility")


# POST a facility with no key-value
def test_post_missing_kv_facility(app_fixture):
    app.logger.info("POST a booking with missing key-value pair")

    # POST test data
    endpoint_response = app_fixture.post('/facility', json={})

    assert endpoint_response.status_code == 400
    decoded_string = json.loads(endpoint_response.data)

    assert decoded_string == {'error': 'No data provided'}

    app.logger.info("END OF TEST: test_post_missing_kv_facility")


# GET a facility with valid facility ID
def test_get_validID_facility(app_fixture):

    app.logger.info("GET a facility with valid ID")

    # POST a facility first
    test_record_1 = app_fixture.post('/facility', json={
        'facilityName': "Swimming Pool",
        'capacity': 30,
        'openingTime': "08:00:00",
        'closingTime': "20:00:00",
        'managerId': "63F0DE4724EF6726E1F27D57"})

    # POST a second facility
    test_record_2 = app_fixture.post('/facility', json={
        'facilityName': "Tennis court",
        'capacity': 4,
        'openingTime': "08:00:00",
        'closingTime': "20:00:00",
        'managerId': "24F01E5793QF9716E1F29E57"})

    decoded_string = json.loads(test_record_1.data)
    testId = decoded_string['id']

    # Attempt to get the facilitt
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

    # POST a facility first
    test_record_1 = app_fixture.post('/facility', json={
        'facilityName': "Swimming Pool",
        'capacity': 30,
        'openingTime': "08:00:00",
        'closingTime': "20:00:00",
        'managerId': "63F0DE4724EF6726E1F27D57"})

    # POST a second facility
    test_record_2 = app_fixture.post('/facility', json={
        'facilityName': "Tennis court 1",
        'capacity': 4,
        'openingTime': "08:00:00",
        'closingTime': "20:00:00",
        'managerId': "24F01E5793QF9716E1F29E57"})

    # Attempt to get the facilitt
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


# GET facility with invalid ID
def test_get_invalidID_facility(app_fixture):

    app.logger.info("GET a facility with invalid ID")

    # POST a facility first
    test_record_1 = app_fixture.post('/facility', json={
        'facilityName': "Swimming Pool",
        'capacity': 30,
        'openingTime': "08:00:00",
        'closingTime': "20:00:00",
        'managerId': "63F0DE4724EF6726E1F27D57"})

    # POST a second facility
    test_record_2 = app_fixture.post('/facility', json={
        'facilityName': "Tennis court",
        'capacity': 4,
        'openingTime': "08:00:00",
        'closingTime': "20:00:00",
        'managerId': "24F01E5793QF9716E1F29E57"})

    decoded_string = json.loads(test_record_1.data)
    testId = decoded_string['id']

    # Attempt to get the facility
    endpoint_response = app_fixture.get(f"/facility/111")
    assert endpoint_response.status_code == 404

    # Decode the returned byte string
    decoded_string = json.loads(endpoint_response.data)
    assert decoded_string == {'error': 'Facility with id 111 does not exist.'}

    app.logger.info("END OF TEST: test_get_invalidID_facility")


# GET a facility with an invalid Facility Name
def test_get_invalidName_facility(app_fixture):

    app.logger.info("GET a facility with an invalid name")

    # POST a facility first
    test_record_1 = app_fixture.post('/facility', json={
        'facilityName': "Swimming Pool",
        'capacity': 30,
        'openingTime': "08:00:00",
        'closingTime': "20:00:00",
        'managerId': "63F0DE4724EF6726E1F27D57"})

    # POST a second facility
    test_record_2 = app_fixture.post('/facility', json={
        'facilityName': "Tennis court 1",
        'capacity': 4,
        'openingTime': "08:00:00",
        'closingTime': "20:00:00",
        'managerId': "24F01E5793QF9716E1F29E57"})

    # Attempt to get the facilitt
    endpoint_response = app_fixture.get("/facility/Tennis court")
    assert endpoint_response.status_code == 404

    # Decode the returned byte string
    decoded_string = json.loads(endpoint_response.data)
    assert decoded_string == {
        'error': 'Facility with id Tennis court does not exist.'}

    app.logger.info("END OF TEST: test_get_invalidName_facility")


# PATCH a valid facility
def test_patch_valid_facility(app_fixture):
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

    app.logger.info("END OF TEST: test_patch_valid_facility")


# PATCH a facility with invalid data
def test_patch_invalid_facility(app_fixture):
    app.logger.info("PATCH a facility with invalid data - wrong data type")

    test_record = app_fixture.post('/facility', json={
        'facilityName': "Swimming Pool",
        'capacity': 30,
        'openingTime': "08:00:00",
        'closingTime': "20:00:00",
        'managerId': "63F0DE4724EF6726E1F27D57"})

    update_record = app_fixture.patch('facility/Swimming Pool', json={
        'capacity': 30,
        'openingTime': "09:AB:00"})

    decoded_string = json.loads(update_record.data)

    assert update_record.status_code == 400
    assert decoded_string == {
        'ValueError': 'Data does not match the required format in one or more fields'}

    app.logger.info("END OF TEST: test_patch_invalid_facility")


# PATCH a facility with missing data
def test_patch_missingData_facility(app_fixture):
    app.logger.info(
        "PATCH a facility with missing data - updating a non existing record")

    update_record = app_fixture.patch('facility/Swimming Pool', json={
        'capacity': 30,
        'openingTime': "09:AB:00"})

    decoded_string = json.loads(update_record.data)

    assert update_record.status_code == 404
    assert decoded_string == {
        'error': 'Facility with id Swimming Pool does not exist.'}

    app.logger.info("END OF TEST: test_patch_missingData_facility")
