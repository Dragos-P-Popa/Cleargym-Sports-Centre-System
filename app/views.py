from app import app, db, models
from flask import json, request, jsonify, abort


# This function is to create a new booking
@app.route('/sales', methods=['POST'])
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
        saleValue=user_input["saleValue"],
        facilityId=user_input["facilityId"],
        activityId=user_input["activityId"])
    db.session.add(new_Sale)
    db.session.commit()
    response = {'id': new_Sale.id,
                'saleValue': new_Sale.saleValue,
                'facilityId': new_Sale.facilityId,
                'activityId': new_Sale.activityId,
                'saleDate': new_Sale.saleDate.strftime('%Y/%m/%d')}
    return jsonify(response), 200


@app.route('/sales', methods=['GET'])
def get_all_sales():
    # get all Sales in the database
    Sales = models.Sales.query.all()
    result = []
    Sales_response(Sales, result)
    return jsonify(result), 200

@app.route('/sales/facility/<int:facilityId>', methods=['GET'])
def get_sales_by_facilityId(facilityId):
    # Requesting the data from the database by using the selected Facilityid
    Sales = models.Sales.query.filter_by(facilityId=facilityId).all()
    result = []
    Sales_response(Sales, result)

    return jsonify(result), 200

@app.route('/sales/activity/<int:activityId>', methods=['GET'])
def get_sales_by_ActivityId(activityId):
    # Requesting the data from the database by using the selected ActivityId
    Sales = models.Sales.query.filter_by(activityId=activityId).all()
    result = []
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
