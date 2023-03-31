from app import app, db, models

from flask import json, request, jsonify, abort
from datetime import datetime, time, date, timedelta
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
import requests


# This function is to create a new booking
@app.route('/sale', methods=['POST'])
def post_sale():
    user_input = request.get_json()

    # Getting all booking in the Database and count them
    all_sales = models.Sales.query.all()
    SaleId = len(all_sales) + 1

    # Giving the booking a booking ID automatically
    for item in all_sales:
        if models.Sales.query.get(SaleId):
            SaleId = SaleId - 1
        elif models.Sales.query.get(SaleId):
            SaleId = SaleId + 1

    new_Sale = models.Sales(
        id=SaleId,
        SaleVal=user_input["SaleVal"],
        Facilityid=user_input["Facilityid"],
        Activityid=user_input["Activityid"]
    )
    db.session.add(new_Sale)
    db.session.commit()
    response = {'id': new_Sale.id,
                'SaleVal': new_Sale.SaleVal,
                'Facilityid': new_Sale.Facilityid,
                'Activityid': new_Sale.Activityid
                }
    return jsonify(response), 200


@app.route('/sales', methods=['POST'])
def get_all_sales():
    # get all Sales in the database
    Sales = models.Sales.query.all()
    result = []
    for sale in Sales:
        result.append({'id': sale.id,
                       'SaleVal': sale.SaleVal,
                       'Facilityid': sale.Facilityid,
                       'Activityid': sale.Activityid
                       })
    return jsonify(result), 200

@app.route('/sales/Facility/<int:Facilityid>', methods=['GET'])
def get_sales_by_facilityId(Facilityid):
    # Requesting the data from the database by using the selected Facilityid
    Sales = models.Sales.query.filter_by(Facilityid=Facilityid).all()
    result = []
    # for each facility, steralise the object given by sqlalchemy
    for sale in Sales:
        result.append({'id': sale.id,
                       'SaleVal': sale.SaleVal,
                       'Facilityid': sale.Facilityid,
                       'Activityid': sale.Activityid
                       })
    # convert to json and return
    return jsonify(result), 200





@app.route('/sales/Activity/<int:ActivityId>', methods=['GET'])
def get_sales_by_ActivityId(ActivityId):
    # Requesting the data from the database by using the selected ActivityId
    Sales = models.Sales.query.filter_by(Activityid=ActivityId).all()
    result = []
    for sale in Sales:
        result.append({'id': sale.id,
                       'SaleVal': sale.SaleVal,
                       'Facilityid': sale.Facilityid,
                       'Activityid': sale.Activityid
                       })
    # convert to json and return
    return jsonify(result), 200
