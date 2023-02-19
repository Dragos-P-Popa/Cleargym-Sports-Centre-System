from app import app

@app.route('/Create')
def create():
    return "create a booking"

@app.route('/Delete')
def Delete():
    return "Delete a booking"

@app.route('/Update')
def Update():
    return "Update a booking"

@app.route('/FindU')
def FindUid():
    return "Find a booking by the user id"

@app.route('/Find')
def FindBid():
    return "Find a booking by the booking id"