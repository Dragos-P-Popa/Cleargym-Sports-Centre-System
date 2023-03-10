from app import app, db, models
from flask import request, jsonify
from datetime import datetime
from create_facilities import preload_data
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError


# Error handlers:
# The error handlers for IntegrityError, KeyError, UnmappedInstanceError,
# TypeError, AttributeError and ValueError.
# These might occur when data is:
# - of an invalid type from the database schema perspective
# - missing from the request
# - refers to a non-existent database record
# - of an invalid type as a function parameter
# - refering to a non-existent attribute, e.g. in a NoneType object
# - sent in an incorrect format (e.g. date/time)

@app.errorhandler(IntegrityError)
def integrity_error_handler(error):
    db.session.rollback()
    app.logger.error(str(error))
    # IntegrityError refers to invalid data type in database operations
    return jsonify({"IntegrityError": "Invalid data in one or more fields"}), 400

@app.errorhandler(KeyError)
def key_error_handler(error):
    db.session.rollback()
    app.logger.error(str(error))
    # KeyError refers to a missing key:value pair
    return jsonify({"KeyError": "Missing data in the request"}), 400

@app.errorhandler(UnmappedInstanceError)
def unmapped_error_handler(error):
    db.session.rollback()
    app.logger.error("UnmappedInstanceError detected")
    # UnmappedInstanceError is raised when trying to operate on a non-existent record
    return jsonify({"UnmappedInstanceError": "Record not found in the database"}), 400

@app.errorhandler(TypeError)
def type_error_handler(error):
    db.session.rollback()
    app.logger.error("TypeError detected")
    # TypeError refers to invalid data type passed as an argument to a function
    return jsonify({"TypeError": "Endpoint function operating on a wrong data type"}), 400

@app.errorhandler(AttributeError)
def attribute_error_handler(error):
    db.session.rollback()
    app.logger.error("AttributeError detected")
    # AttributeError is raised when trying to access an attribute
    # of a NoneType object assigned to a variable in views.py
    return jsonify({"AttributeError": "The referenced record does not exist"}), 400

@app.errorhandler(ValueError)
def value_error_handler(error):
    db.session.rollback()
    app.logger.error("ValueError detected")
    # ValueError is raised when the sent data does not match the required format
    # e.g. date/time
    return jsonify({"ValueError": "Data does not match the required format in one or more fields"}), 400


# create the table and the database before running the first request
@app.before_first_request
def create_tables():
    # preload some data in the database
    preload_data()

# API endpoint that shows a facility either by facility id or facility name
@app.route('/facility/<param>', methods=['GET'])
def get_facility(param):
    facility = None
    if param.isdigit():
        # parameter is a facility ID
        facility = db.session.query(models.Facility).filter_by(id=int(param)).first()
    else:
        # parameter is a name of facility
        facility = db.session.query(models.Facility).filter_by(facilityName=param).first()
    if facility is None:
        #  if the code does not run correctly, return a 404 Not Found status code
        return jsonify({'error': f'Facility with id {param} does not exist.'}), 404
    
    # return facility
    result = {  'id': facility.id,
                'facilityName': facility.facilityName,
                'capacity': facility.capacity,
                'openingTime': facility.openingTime.strftime('%H:%M:%S'),
                'closingTime': facility.closingTime.strftime('%H:%M:%S'),
                'managerId': facility.managerId   }

    # if the code runs correctly, return an 200 OK status code
    return jsonify(result), 200


# API endpoint that allows to change specific values of a facility on facility id or facility name
@app.route('/facility/<param>', methods=['PATCH'])
def update_facility(param):
    facility = None
    if param.isdigit():
        # parameter is a facility ID
        facility = db.session.query(models.Facility).filter_by(id=int(param)).first()
    else:
        # parameter is a name of facility
        facility = db.session.query(models.Facility).filter_by(facilityName=param).first()
    if facility is None:
        #  if the code does not run correctly, return a 404 Not Found status code
        return jsonify({'error': f'Facility with id {param} does not exist.'}), 404
    
    # retrieve data
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # update facility properties with new values from request data
    if 'facilityName' in data:
        facility.facilityName = data['facilityName']
    if 'capacity' in data:
        facility.capacity = data['capacity']
    if 'openingTime' in data:
        facility.openingTime = datetime.strptime(data['openingTime'], '%H:%M:%S').time()
    if 'closingTime' in data:
        facility.closingTime = datetime.strptime(data['closingTime'], '%H:%M:%S').time()
    if 'managerId' in data:
        facility.managerId = data['managerId']

    # commit changes to the database
    db.session.commit()

    # return updated facility
    result = {  'id': facility.id,
                'facilityName': facility.facilityName,
                'capacity': facility.capacity,
                'openingTime': facility.openingTime.strftime('%H:%M:%S'),
                'closingTime': facility.closingTime.strftime('%H:%M:%S'),
                'managerId': facility.managerId   }

    # if the code runs correctly, return an 200 OK status code
    return jsonify(result), 200


# API endpoint to create a new facility
@app.route('/facility', methods=['POST'])
def create_facility():
    # retrieve data from request body
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # create a new Facility object with the provided data
    facility = models.Facility(
        facilityName=data['facilityName'],
        capacity=data['capacity'],
        openingTime=datetime.strptime(data['openingTime'], '%H:%M:%S').time(),
        closingTime=datetime.strptime(data['closingTime'], '%H:%M:%S').time(),
        managerId=data['managerId']
    )
    
    # add new facility to the database
    db.session.add(facility)
    db.session.commit()
    
    # return the new facility as a response
    result = {  'id': facility.id,
                'facilityName': facility.facilityName,
                'capacity': facility.capacity,
                'openingTime': facility.openingTime.strftime('%H:%M:%S'),
                'closingTime': facility.closingTime.strftime('%H:%M:%S'),
                'managerId': facility.managerId   }
    
    # if the code runs correctly, return an 200 OK status code
    return jsonify(result), 200

# API endpoint for fetching all facilities
@app.route('/facilities', methods=['GET'])
def get_all_facilities():
    # get all facilities in the database
    facilities = models.Facility.query.all()
    # initialise list
    result = []

    # for each facility, steralise the object given by sqlalchemy
    for facility in facilities:
        result.append({  'id': facility.id,
            'facilityName': facility.facilityName,
            'capacity': facility.capacity,
            'openingTime': facility.openingTime.strftime('%H:%M:%S'),
            'closingTime': facility.closingTime.strftime('%H:%M:%S'),
            'managerId': facility.managerId   })

    # convert to json and return
    return jsonify(result), 200
