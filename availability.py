from flask import abort
import datetime
from datetime import datetime, time, date, timedelta
from app import app, db, models
from flask import json, request, jsonify, abort


class Booking:

    def __init__(self, Bdate, Btime, Blength, Bend, FacilityId, Close, Open, Capacity, A_time, A_end, Alength, A_day
                 ):
        self.Bdate = Bdate
        self.Btime = Btime
        self.Blength = Blength
        self.Bend = Bend
        self.FacilityId = FacilityId
        self.Open = Open
        self.Close = Close
        self.Capacity = Capacity
        self.A_time = A_time
        self.A_end = A_end
        self.Alength = Alength
        self.A_day = A_day

    # length_one is a function that accepts or refuses a
    # booking that has 1 hour length.
    def length_one(self, Bdate, Btime, Bend, Capacity, FacilityId):

        twohours = time(2, 0, 0)
        # here i had bend + 2

        # All Bookings that starts at booking start time.
        a1 = models.Booking.query.filter_by(bookingDate=Bdate,
                                            bookingTime=Btime,
                                            facilityId=FacilityId).all()

        # All Bookings that starts booking start time and ends in one hour
        a2 = models.Booking.query.filter_by(bookingDate=Bdate,
                                            bookingTime=Btime,
                                            bookingEndTime=Bend,
                                            facilityId=FacilityId
                                            ).all()

        # All bookings that ends after 1 hour of booking start time
        a3 = models.Booking.query.filter_by(bookingDate=Bdate,
                                            bookingEndTime=Bend,
                                            facilityId=FacilityId
                                            ).all()
        b1 = len(a1)
        b2 = len(a2)
        b3 = len(a3)

        Block1 = (b1 + b2) - b3
        Block2 = Block3 = 0

        if Block1 >= Capacity:
            abort(400, description='Full Capacity in the first part of your Booking')
        elif Block2 >= Capacity:
            abort(400, description='Full Capacity in the second part of your Booking')
        elif Block3 >= Capacity:
            abort(400, description='Full Capacity in the third part of your Booking')
        else:
            return True
        return True

    # length_two is a function that accepts or refuses a booking that has 2 hours length
    def length_two(self, Bdate, Btime, Bend, Capacity, FacilityId):

        onehour = time(1, 0, 0)
        twohours = time(2, 0, 0)

        # x is the hour before the booking end time.
        x = (datetime.combine(datetime.today(), Bend)
             - timedelta(hours=onehour.hour, minutes=onehour.minute, seconds=onehour.second)).time()

        y = (datetime.combine(datetime.today(), Bend)
             + timedelta(hours=twohours.hour, minutes=twohours.minute, seconds=twohours.second)).time()

        # all booking that ends at end time
        a1 = models.Booking.query.filter_by(bookingDate=Bdate,
                                            bookingEndTime=Bend,
                                            facilityId=FacilityId
                                            ).all()
        # all booking that ends 1 hour  before the end time
        a2 = models.Booking.query.filter_by(bookingDate=Bdate,
                                            bookingEndTime=x,
                                            facilityId=FacilityId
                                            ).all()
        # all bookings that starts 1 hour before end time
        a3 = models.Booking.query.filter_by(bookingDate=Bdate,
                                            bookingTime=x,
                                            facilityId=FacilityId
                                            ).all()
        # All Bookings that starts at booking start time.
        a4 = models.Booking.query.filter_by(bookingDate=Bdate,
                                            bookingTime=Btime,
                                            facilityId=FacilityId
                                            ).all()

        # All Bookings that starts booking start time and ends in one hour
        a5 = models.Booking.query.filter_by(bookingDate=Bdate,
                                            bookingTime=Btime,
                                            bookingEndTime=x,
                                            facilityId=FacilityId
                                            ).all()
        # All Bookings that starts at New booking start time + 1 Hour and ends at New booking ends time
        a6 = models.Booking.query.filter_by(bookingDate=Bdate,
                                            bookingTime=x,
                                            bookingEndTime=Bend,
                                            facilityId=FacilityId
                                            ).all()

        b1 = len(a1)
        b2 = len(a2)
        b3 = len(a3)
        b4 = len(a4)
        b5 = len(a5)
        b6 = len(a6)

        Block2 = (b1 + b3) - b6
        Block1 = (b4 + b2) - b5
        Block3 = 0

        if Block1 >= Capacity:
            abort(400, description='Full Capacity in the first part of your Booking')
        elif Block2 >= Capacity:
            abort(400, description='Full Capacity in the second part of your Booking')
        elif Block3 >= Capacity:
            abort(400, description='Full Capacity in the third part of your Booking')
        else:
            return True
        return True

    # length_one is a function that accepts or refuses a booking that has 3 hours length
    def length_three(self, Bdate, Btime, Bend, Capacity, FacilityId):

        onehour = time(1, 0, 0)
        twohours = time(2, 0, 0)

        x = (datetime.combine(datetime.today(), Bend)
             - timedelta(hours=onehour.hour, minutes=onehour.minute, seconds=onehour.second)).time()

        y = (datetime.combine(datetime.today(), Bend)
             - timedelta(hours=twohours.hour, minutes=twohours.minute, seconds=twohours.second)).time()

        # Block 1
        # All Bookings that starts at booking start time.
        a1 = models.Booking.query.filter_by(bookingDate=Bdate,
                                            bookingTime=Btime,
                                            facilityId=FacilityId
                                            ).all()

        # All Bookings that starts booking start time and ends in one hour
        a2 = models.Booking.query.filter_by(bookingDate=Bdate,
                                            bookingTime=Btime,
                                            bookingEndTime=y,
                                            facilityId=FacilityId
                                            ).all()

        # All bookings that ends after 1 hour of booking start time
        a3 = models.Booking.query.filter_by(bookingDate=Bdate,
                                            bookingEndTime=y,
                                            facilityId=FacilityId
                                            ).all()
        # Block 2
        # All bookings that starts 1 hour after booking start time
        a4 = models.Booking.query.filter_by(bookingDate=Bdate,
                                            bookingTime=y,
                                            facilityId=FacilityId
                                            ).all()

        # All booking that ends 1 hour before the end time
        a5 = models.Booking.query.filter_by(bookingDate=Bdate,
                                            bookingEndTime=x,
                                            facilityId=FacilityId
                                            ).all()

        a6 = models.Booking.query.filter_by(bookingDate=Bdate,
                                            bookingTime=x,
                                            bookingEndTime=x,
                                            facilityId=FacilityId
                                            ).all()
        # Block 3
        # All booking that starts after 2 hours
        a7 = models.Booking.query.filter_by(bookingDate=Bdate,
                                            bookingTime=x,
                                            facilityId=FacilityId
                                            ).all()

        # All booking that ends at Booking end time
        a8 = models.Booking.query.filter_by(bookingDate=Bdate,
                                            bookingEndTime=Bend,
                                            facilityId=FacilityId
                                            ).all()

        # All booking that starts after 2 hours and ends at Booking end time
        a9 = models.Booking.query.filter_by(bookingDate=Bdate,
                                            bookingTime=x,
                                            bookingEndTime=Bend,
                                            facilityId=FacilityId
                                            ).all()

        b1 = len(a1)
        b2 = len(a2)
        b3 = len(a3)
        b4 = len(a4)
        b5 = len(a5)
        b6 = len(a6)
        b7 = len(a7)
        b8 = len(a8)
        b9 = len(a9)

        Block1 = (b1 + b2) - b3
        Block2 = (b4 + b5) - b6
        Block3 = (b7 + b8) - b9

        if Block1 >= Capacity:
            abort(400, description='Full Capacity in the first part of your Booking')
        elif Block2 >= Capacity:
            abort(400, description='Full Capacity in the second part of your Booking')
        elif Block3 >= Capacity:
            abort(400, description='Full Capacity in the third part of your Booking')
        else:
            return True
        return True

    # check Facility
    def check_facility_capacity(self, Bdate, Btime, Bend, Capacity, FacilityId, Blength):
        onehour = time(1, 0, 0)
        twohours = time(2, 0, 0)
        threehours = time(3, 0, 0)

        if Blength == onehour:
            Booking.length_one(self, Bdate, Btime, Bend, Capacity, FacilityId)
        elif Blength == twohours:
            Booking.length_two(self, Bdate, Btime, Bend, Capacity, FacilityId)
        elif Blength == threehours:
            Booking.length_three(self, Bdate, Btime, Bend, Capacity, FacilityId)
        else:
            abort(400, description='Invalid Length')

    def check_facility_time(self, Btime, Bend, Open, Close):

        if Close > Btime > Open and Close > Bend > Open:
            return True
        else:
            abort(400, description=' Too Early / Late')

    # check Facility done
    # Activity Check Begins

    def check_activity(self, Alength, A_day, Blength, Bdate, Btime, Bend, A_time, A_end):

        day_name = Bdate.strftime('%A')

        if A_time > Btime:
            abort(400, description='Invalid Start Time')
        if Btime > A_end:
            abort(400, description='Invalid Start Time')
        if A_time > Bend:
            abort(400, description='Invalid End Time')
        if Bend > A_end:
            abort(400, description='Invalid End Time')
        if Alength < Blength:
            abort(400, description='Invalid Length')
        if A_day != "ANY" and A_day != day_name:
            abort(400, description='Invalid Day')
        else:
            return True


# Activity Check Ends
