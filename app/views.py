# This Code made by BOUHAMADI Mohamed Yanis
from app import app, db, models
from flask import json, request, jsonify, abort

@app.route('/sales', methods=['POST'])
# post_sale() is an endpoint for adding sales made to the database
def post_sale():
    # Requesting data
    user_input = request.get_json()
    # This block of code is to manipulate with the sale id in the database
    all_sales = models.Sales.query.all()
    SaleId = len(all_sales) + 1
    for item in all_sales:
        if models.Sales.query.get(SaleId):
            SaleId = SaleId - 1
        elif models.Sales.query.get(SaleId):
            SaleId = SaleId + 1
    # Creating a new sale
    new_Sale = models.Sales(
        id=SaleId,
        saleValue=user_input["saleValue"],
        facilityId=user_input["facilityId"],
        activityId=user_input["activityId"])
    # Adding the new sale to the database
    db.session.add(new_Sale)
    db.session.commit()
    # Returning the sale details as a response
    response = {'id': new_Sale.id,
                'saleValue': new_Sale.saleValue,
                'facilityId': new_Sale.facilityId,
                'activityId': new_Sale.activityId,
                'saleDate': new_Sale.saleDate.strftime('%Y/%m/%d')}
    return jsonify(response), 200


@app.route('/sales', methods=['GET'])
def get_all_sales():
    # Get all Sales in the database
    Sales = models.Sales.query.all()
    #  Create an empty list
    result = []
    # Add the gotten sales to the list and return the list
    Sales_response(Sales, result)
    return jsonify(result), 200

@app.route('/sales/facility/<int:facilityId>', methods=['GET'])
def get_sales_by_facilityId(facilityId):
    # Requesting the data from the database by using the selected Facilityid
    Sales = models.Sales.query.filter_by(facilityId=facilityId).all()
    #  Create an empty list
    result = []
    # Add the gotten sales to the list and return the list
    Sales_response(Sales, result)
    return jsonify(result), 200

@app.route('/sales/activity/<int:activityId>', methods=['GET'])
def get_sales_by_ActivityId(activityId):
    # Requesting the data from the database by using the selected ActivityId
    Sales = models.Sales.query.filter_by(activityId=activityId).all()
    #  Create an empty list
    result = []
    # Add the gotten sales to the list and return the list
    Sales_response(Sales, result)
    return jsonify(result), 200

def Sales_response(Sales, result):
    for sale in Sales:
        result.append({'id': sale.id,
                       'saleValue': sale.saleValue,
                       'facilityId': sale.facilityId,
                       'activityId': sale.activityId,
                       'saleDate': sale.saleDate.strftime('%Y/%m/%d')
                       })
