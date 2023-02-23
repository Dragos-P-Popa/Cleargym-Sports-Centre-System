from app import app, db, models
from flask import Flask, request
from datetime import datetime


# @app.before_first_request
# def create_tables():
#     db.create_all()

# API endpoint that shows a facility either by facility id or facility name
@app.route('/facility/<param>', methods=['GET'])
def get_facility(param):
    facility = None
    if param.isdigit():
        # parameter is a facility ID
        facility = db.Facility.query.filter_by(id=int(param)).first()
    else:
        # parameter is a name of facility
        facility = db.Facility.query.filter_by(facilityName=param).first()
    if facility is None:
        #  if the code does not run correctly, return a 404 Not Found status code
        return {'error': f'Facility with id {param} does not exist.'}, 404
    
    # return facility
    result = {  'id': facility.id,
                'facilityName': facility.facilityName,
                'capacity': facility.capacity,
                'opening_time': facility.opening_time.strftime('%H:%M:%S'),
                'closing_time': facility.closing_time.strftime('%H:%M:%S'),
                'manager_id': facility.manager_id   }

    # if the code runs correctly, return an 200 OK status code
    return {'facility': result}, 200


# API endpoint that allows to change specific values of a facility on facility id or facility name
@app.route('/facility/<param>', methods=['PATCH'])
def update_facility(param):
    facility = None
    if param.isdigit():
        # parameter is a facility ID
        facility = db.Facility.query.filter_by(id=int(param)).first()
    else:
        # parameter is a name of facility
        facility = db.Facility.query.filter_by(facilityName=param).first()
    if facility is None:
        #  if the code does not run correctly, return a 404 Not Found status code
        return {'error': f'Facility with id {param} does not exist.'}, 404
    
    # retrieve data, not sure if this is correct (?)
    data = request.get_json()
    if not data:
        return {'error': 'No data provided'}, 400

    # update facility properties with new values from request data
    if 'facilityName' in data:
        facility.facilityName = data['facilityName']
    if 'capacity' in data:
        facility.capacity = data['capacity']
    if 'opening_time' in data:
        facility.opening_time = datetime.strptime(data['opening_time'], '%H:%M:%S').time()
    if 'closing_time' in data:
        facility.closing_time = datetime.strptime(data['closing_time'], '%H:%M:%S').time()
    if 'manager_id' in data:
        facility.manager_id = data['manager_id']

    # commit changes to the database
    db.session.commit()

    # return updated facility
    result = {  'id': facility.id,
                'facilityName': facility.facilityName,
                'capacity': facility.capacity,
                'opening_time': facility.opening_time.strftime('%H:%M:%S'),
                'closing_time': facility.closing_time.strftime('%H:%M:%S'),
                'manager_id': facility.manager_id   }

    # if the code runs correctly, return an 200 OK status code
    return {'facility': result}, 200


# API endpoint to create a new facility
@app.route('/facility', methods=['POST'])
def create_facility():
    # retrieve data from request body
    data = request.get_json()
    if not data:
        return {'error': 'No data provided'}, 400
    
    # create a new Facility object with the provided data
    facility = models.Facility(
        facilityName=data['facilityName'],
        capacity=data['capacity'],
        opening_time=datetime.strptime(data['opening_time'], '%H:%M:%S').time(),
        closing_time=datetime.strptime(data['closing_time'], '%H:%M:%S').time(),
        manager_id=data['manager_id']
    )
    
    # add new facility to the database
    db.session.add(facility)
    db.session.commit()
    
    # return the new facility as a response
    result = {  'id': facility.id,
                'facilityName': facility.facilityName,
                'capacity': facility.capacity,
                'opening_time': facility.opening_time.strftime('%H:%M:%S'),
                'closing_time': facility.closing_time.strftime('%H:%M:%S'),
                'manager_id': facility.manager_id   }
    
    # if the code runs correctly, return an 200 OK status code
    return {'facility': result}, 200
