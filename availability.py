from flask import abort
import datetime
from datetime import datetime, time, date, timedelta
from app import app, db, models


class Booking:
    def __init__(self, Bdate, Btime, Blength, Bend, Btype, FacilityId, Close, Open, Capacity):
        self.Bdate = Bdate
        self.Btime = Btime
        self.Blength = Blength
        self.Bend = Bend
        self.Btype = Btype
        self.FacilityId = FacilityId
        self.Open = Open
        self.Close = Close
        self.Capacity = Capacity

    def check_time(self, Btime, Bend, Open, Close):

        if Close > Btime > Open and Close > Bend > Open:
            return True
        else:
            abort(400, description='Too Early / Late')

    # length_one is a function that accepts or refuses a
    # booking that has 1 hour length.
    def length_one(self, booking, Bdate, Btime, Blength, Bend, Btype, Capacity):

        start = datetime.combine(datetime.today(), Btime)
        end = datetime.combine(datetime.today(), Bend)
        onehour = time(1, 0, 0)
        twohours = time(2, 0, 0)

        moins_un = (datetime.combine(datetime.today(), Bend)
                    - timedelta(hours=onehour.hour, minutes=onehour.minute, seconds=onehour.second)).time()

        moins_deux = (datetime.combine(datetime.today(), Bend)
                      + timedelta(hours=twohours.hour, minutes=twohours.minute, seconds=twohours.second)).time()

        # All Bookings that starts at booking start time.
        a1 = models.Booking.query.filter_by(bookingDate=booking.bookingDate,
                                            bookingTime=Btime,
                                            bookingType=Btype).all()

        # All Bookings that starts booking start time and ends in one hour
        a2 = models.Booking.query.filter_by(bookingDate=booking.bookingDate,
                                            bookingTime=Btime,
                                            bookingEndTime=moins_deux,
                                            bookingType=Btype).all()

        # All bookings that ends after 1 hour of booking start time
        a3 = models.Booking.query.filter_by(bookingDate=booking.bookingDate,
                                            bookingEndTime=moins_deux,
                                            bookingType=Btype).all()
        b1 = len(a1)
        b2 = len(a2)
        b3 = len(a3)

        Block1 = (b1 + b2) - b3
        Block2 = Block3 = 0

        if Block1 >= Capacity:
            abort(400, description='Invalid time Block 1')
        else:
            return True

        return Block1, Block2, Block3

    # length_two is a function that accepts or refuses a booking that has 2 hours length
    def length_two(self, booking, Bdate, Btime, Blength, Bend, Btype, Capacity):

        start = datetime.combine(datetime.today(), Btime)
        end = datetime.combine(datetime.today(), Bend)
        onehour = time(1, 0, 0)
        twohours = time(2, 0, 0)

        moins_un = (datetime.combine(datetime.today(), Bend)
                    - timedelta(hours=onehour.hour, minutes=onehour.minute, seconds=onehour.second)).time()

        moins_deux = (datetime.combine(datetime.today(), Bend)
                      + timedelta(hours=twohours.hour, minutes=twohours.minute, seconds=twohours.second)).time()

        # all booking that ends at end time
        a = models.Booking.query.filter_by(bookingDate=booking.bookingDate,
                                           bookingEndTime=Bend,
                                           bookingType=booking.bookingType).all()
        # all booking that ends 1 hour  before the end time
        b = models.Booking.query.filter_by(bookingDate=booking.bookingDate,
                                           bookingEndTime=moins_un,
                                           bookingType=Btype).all()
        # all bookings that starts 1 hour before end time
        c = models.Booking.query.filter_by(bookingDate=booking.bookingDate,
                                           bookingTime=moins_un,
                                           bookingType=Btype).all()
        # All Bookings that starts at booking start time.
        d = models.Booking.query.filter_by(bookingDate=booking.bookingDate,
                                           bookingTime=Btime,
                                           bookingType=Btype).all()

        # All Bookings that starts booking start time and ends in one hour
        e = models.Booking.query.filter_by(bookingDate=booking.bookingDate,
                                           bookingTime=Btime,
                                           bookingEndTime=moins_un,
                                           bookingType=Btype).all()
        # All Bookings that starts at New booking start time + 1 Hour and ends at New booking ends time
        f = models.Booking.query.filter_by(bookingDate=booking.bookingDate,
                                           bookingTime=moins_un,
                                           bookingEndTime=Bend,
                                           bookingType=Btype).all()

        aa = len(a)
        bb = len(b)
        cc = len(c)
        dd = len(d)
        ee = len(e)
        ff = len(f)

        Block2 = (aa + cc) - ff
        Block1 = (dd + bb) - ee
        Block3 = 0

        if Block1 >= Capacity:
            abort(400, description='Full Capacity in the first part of your Booking')
        elif Block2 >= Capacity:
            abort(400, description='Full Capacity in the second part of your Booking')
        else:
            return True

        return Block1, Block2, Block3

    # length_one is a function that accepts or refuses a booking that has 3 hours length
    def length_three(self, booking, Bdate, Btime, Blength, Bend, Btype, Capacity):

        start = datetime.combine(datetime.today(), Btime)
        end = datetime.combine(datetime.today(), Bend)
        onehour = time(1, 0, 0)
        twohours = time(2, 0, 0)

        moins_un = (datetime.combine(datetime.today(), Bend)
                    - timedelta(hours=onehour.hour, minutes=onehour.minute, seconds=onehour.second)).time()

        moins_deux = (datetime.combine(datetime.today(), Bend)
                      - timedelta(hours=twohours.hour, minutes=twohours.minute, seconds=twohours.second)).time()

        # Block 1
        # All Bookings that starts at booking start time.
        a1 = models.Booking.query.filter_by(bookingDate=booking.bookingDate,
                                            bookingTime=Btime,
                                            bookingType=Btype).all()

        # All Bookings that starts booking start time and ends in one hour
        a2 = models.Booking.query.filter_by(bookingDate=booking.bookingDate,
                                            bookingTime=Btime,
                                            bookingEndTime=moins_deux,
                                            bookingType=Btype).all()

        # All bookings that ends after 1 hour of booking start time
        a3 = models.Booking.query.filter_by(bookingDate=booking.bookingDate,
                                            bookingEndTime=moins_deux,
                                            bookingType=Btype).all()
        # Block 2
        # All bookings that starts 1 hour after booking start time
        a4 = models.Booking.query.filter_by(bookingDate=booking.bookingDate,
                                            bookingTime=moins_deux,
                                            bookingType=Btype).all()

        # All booking that ends 1 hour before the end time
        a5 = models.Booking.query.filter_by(bookingDate=booking.bookingDate,
                                            bookingEndTime=moins_un,
                                            bookingType=Btype).all()

        a6 = models.Booking.query.filter_by(bookingDate=booking.bookingDate,
                                            bookingTime=moins_un,
                                            bookingEndTime=moins_un,
                                            bookingType=Btype).all()
        # Block 3
        # All booking that starts after 2 hours
        a7 = models.Booking.query.filter_by(bookingDate=booking.bookingDate,
                                            bookingTime=moins_un,
                                            bookingType=Btype).all()

        # All booking that ends at Booking end time
        a8 = models.Booking.query.filter_by(bookingDate=booking.bookingDate,
                                            bookingEndTime=Bend,
                                            bookingType=Btype).all()

        # All booking that starts after 2 hours and ends at Booking end time
        a9 = models.Booking.query.filter_by(bookingDate=booking.bookingDate,
                                            bookingTime=moins_un,
                                            bookingEndTime=Bend,
                                            bookingType=Btype).all()

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
        return Block1, Block2, Block3

    def check_length(self, booking, Bdate, Btime, Blength, Bend, Btype, Capacity):
        onehour = time(1, 0, 0)
        twohours = time(2, 0, 0)
        threehours = time(3, 0, 0)

        if Blength == onehour:
            Booking.length_one(self, booking, Bdate, Btime, Blength, Bend, Btype, Capacity)
        elif Blength == twohours:
            Booking.length_two(self, booking, Bdate, Btime, Blength, Bend, Btype, Capacity)
        elif Blength == threehours:
            Booking.length_three(self, booking, Bdate, Btime, Blength, Bend, Btype, Capacity)
        else:
            abort(400, description='Invalid Length')
