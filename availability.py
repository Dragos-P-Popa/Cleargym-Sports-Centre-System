from flask import abort
import datetime
from datetime import datetime, time, date, timedelta
from app import app, db, models


class Booking:
    def __init__(self, Bdate, Btime, Blength, Bend, Btype):
        self.Bdate = Bdate
        self.Btime = Btime
        self.Blength = Blength
        self.Bend = Bend
        self.Btype = Btype

     # length_one is a function that accepts or refuses a
    # booking that has 1 hour length.
    def length_one(self, booking, Bdate, Btime, Blength, Bend, Btype):

        start = datetime.combine(datetime.today(), Btime)
        end = datetime.combine(datetime.today(), Bend)
        onehour = time(1, 0, 0)
        twohours = time(2, 0, 0)

        moins_un = (datetime.combine(datetime.today(), Bend)
                    - timedelta(hours=onehour.hour, minutes=onehour.minute, seconds=onehour.second)).time()

        moins_deux = (datetime.combine(datetime.today(), Bend)
                      + timedelta(hours=twohours.hour, minutes=twohours.minute, seconds=twohours.second)).time()

        # All Bookings that starts at booking start time.
        a1 = models.Reservation.query.filter_by(bookingDate=booking.bookingDate,
                                                bookingTime=Btime,
                                                bookingType=Btype).all()

        # All Bookings that starts booking start time and ends in one hour
        a2 = models.Reservation.query.filter_by(bookingDate=booking.bookingDate,
                                                bookingTime=Btime,
                                                bookingEndTime=moins_deux,
                                                bookingType=Btype).all()

        # All bookings that ends after 1 hour of booking start time
        a3 = models.Reservation.query.filter_by(bookingDate=booking.bookingDate,
                                                bookingEndTime=moins_deux,
                                                bookingType=Btype).all()
        b1 = len(a1)
        b2 = len(a2)
        b3 = len(a3)

        Block1 = (b1 + b2) - b3
        Block2 = Block3 = 0

        if Block1 >= 3 and Btype == "Swimming pool":
            abort(400, description='Invalid time Block 1')
        else:
            return True

        return Block1, Block2, Block3

    # length_two is a function that accepts or refuses a booking that has 2 hours length
    def length_two(self, booking, Bdate, Btime, Blength, Bend, Btype):

        start = datetime.combine(datetime.today(), Btime)
        end = datetime.combine(datetime.today(), Bend)
        onehour = time(1, 0, 0)
        twohours = time(2, 0, 0)

        moins_un = (datetime.combine(datetime.today(), Bend)
                    - timedelta(hours=onehour.hour, minutes=onehour.minute, seconds=onehour.second)).time()

        moins_deux = (datetime.combine(datetime.today(), Bend)
                      + timedelta(hours=twohours.hour, minutes=twohours.minute, seconds=twohours.second)).time()

        # all booking that ends at end time
        a = models.Reservation.query.filter_by(bookingDate=booking.bookingDate,
                                               bookingEndTime=Bend,
                                               bookingType=booking.bookingType).all()
        # all booking that ends 1 hour  before the end time
        b = models.Reservation.query.filter_by(bookingDate=booking.bookingDate,
                                               bookingEndTime=moins_un,
                                               bookingType=Btype).all()
        # all bookings that starts 1 hour before end time
        c = models.Reservation.query.filter_by(bookingDate=booking.bookingDate,
                                               bookingTime=moins_un,
                                               bookingType=Btype).all()
        # All Bookings that starts at booking start time.
        d = models.Reservation.query.filter_by(bookingDate=booking.bookingDate,
                                               bookingTime=Btime,
                                               bookingType=Btype).all()

        # All Bookings that starts booking start time and ends in one hour
        e = models.Reservation.query.filter_by(bookingDate=booking.bookingDate,
                                               bookingTime=Btime,
                                               bookingEndTime=moins_un,
                                               bookingType=Btype).all()
        # All Bookings that starts at New booking start time + 1 Hour and ends at New booking ends time
        f = models.Reservation.query.filter_by(bookingDate=booking.bookingDate,
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

        if Block1 >= 3 and Btype == "Swimming pool":
            abort(400, description='Invalid time Block 1')
        elif Block2 >= 3 and Btype == "Swimming pool":
            abort(400, description='Invalid time Block 2')
        else:
            return True

        return Block1, Block2, Block3

    # length_one is a function that accepts or refuses a booking that has 3 hours length
    def length_three(self, booking, Bdate, Btime, Blength, Bend, Btype):

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
        a1 = models.Reservation.query.filter_by(bookingDate=booking.bookingDate,
                                                bookingTime=Btime,
                                                bookingType=Btype).all()

        # All Bookings that starts booking start time and ends in one hour
        a2 = models.Reservation.query.filter_by(bookingDate=booking.bookingDate,
                                                bookingTime=Btime,
                                                bookingEndTime=moins_deux,
                                                bookingType=Btype).all()

        # All bookings that ends after 1 hour of booking start time
        a3 = models.Reservation.query.filter_by(bookingDate=booking.bookingDate,
                                                bookingEndTime=moins_deux,
                                                bookingType=Btype).all()
        # Block 2
        # All bookings that starts 1 hour after booking start time
        a4 = models.Reservation.query.filter_by(bookingDate=booking.bookingDate,
                                                bookingTime=moins_deux,
                                                bookingType=Btype).all()

        # All booking that ends 1 hour before the end time
        a5 = models.Reservation.query.filter_by(bookingDate=booking.bookingDate,
                                                bookingEndTime=moins_un,
                                                bookingType=Btype).all()

        a6 = models.Reservation.query.filter_by(bookingDate=booking.bookingDate,
                                                bookingTime=moins_un,
                                                bookingEndTime=moins_un,
                                                bookingType=Btype).all()
        # Block 3
        # All booking that starts after 2 hours
        a7 = models.Reservation.query.filter_by(bookingDate=booking.bookingDate,
                                                bookingTime=moins_un,
                                                bookingType=Btype).all()

        # All booking that ends at Booking end time
        a8 = models.Reservation.query.filter_by(bookingDate=booking.bookingDate,
                                                bookingEndTime=Bend,
                                                bookingType=Btype).all()

        # All booking that starts after 2 hours and ends at Booking end time
        a9 = models.Reservation.query.filter_by(bookingDate=booking.bookingDate,
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
        print(Block1, Block2, Block3)

        if Block1 >= 3 and Btype == "Swimming pool":
            abort(400, description='Invalid time Block 1')
        elif Block2 >= 3 and Btype == "Swimming pool":
            abort(400, description='Invalid time Block 2')
        elif Block3 >= 3 and Btype == "Swimming pool":
            abort(400, description='Invalid time Block 3')
        else:
            return True
        return Block1, Block2, Block3

    def check_activity(self, Btype):

        if self.Btype == "Swimming pool":
            return True
        elif self.Btype == "Fitness room":
            return True
        elif self.Btype == "Sports hall":
            return True
        elif self.Btype == "Studio":
            return True
        elif self.Btype == "Climbing wall":
            return True
        else:
            abort(400, description='Invalid Facility')

    def check_time(self, Btime, Blength, Btype):

        openning_time = time(8, 0, 0)
        ten_am = time(10, 0, 0)
        eight_pm = time(20, 0, 0)
        closing_time = time(22, 0, 0)
        booking_ending_time = (datetime.combine(datetime.today(), Btime)
                               + timedelta(hours=Blength.hour, minutes=Blength.minute, seconds=Blength.second)).time()

        if self.Btype == "Swimming pool" and eight_pm > Btime > openning_time and eight_pm > booking_ending_time > openning_time:
            return True
        elif self.Btype == "Fitness room" and closing_time > Btime > openning_time and closing_time > booking_ending_time > openning_time:
            return True
        elif self.Btype == "Sports hall" and closing_time > Btime > openning_time and closing_time > booking_ending_time > openning_time:
            return True
        elif self.Btype == "Studio" and closing_time > Btime > openning_time and closing_time > booking_ending_time > openning_time:
            return True
        elif self.Btype == "Climbing wall" and eight_pm > Btime > ten_am and eight_pm > booking_ending_time > ten_am:
            return True
        else:
            abort(400, description='Invalid time')

    # def check_availability(self, booking, Bdate, Btime, Blength, Btype):

    # time_plus_one = (datetime.combine(datetime.today(), Btime) + timedelta(hours=Hone.hour, minutes=Hone.minute,seconds=Hone.second)).time()
