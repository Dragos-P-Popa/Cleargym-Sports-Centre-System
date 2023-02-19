import unittest 
from facilities import app
from datetime import datetime

class FacilitiesTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config')
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        #the basedir lines could be added like the original db
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

        pass


    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_new_facility(self):
        #testing by adding a new facility with the right data
        status_code = app.create_facility('Swimming pool', 30, 10.00, '8:00:00', '10:00:00', '63F0DE4724EF6726E1F27D57')
        # self.assertIsInstance(facility_id, int)
        self.assertEqual(status_code, 200) #200 - ok 201- accepted

        #testing by adding invalid capacity
        with self.assertRaises(TypeError):
            status_code = app.create_facility('Swimming pool', 'A' , 10.00, '8:00:00', '10:00:00', '63F0DE4724EF6726E1F27D57')
            self.assertEqual(status_code, 400) #400 Bad request
        
        #testing by adding invalid price
        with self.assertRaises(TypeError):
            status_code = app.create_facility('Swimming pool', 30, 'B', '8:00:00', '10:00:00', '63F0DE4724EF6726E1F27D57')
            self.assertEqual(status_code, 400) #400 Bad request

        #testing by adding invalid opening time
        with self.assertRaises(TypeError):
            status_code = app.create_facility('Swimming pool', 30, 10.00, '8A:00', '10:00:00', '63F0DE4724EF6726E1F27D57')
            self.assertEqual(status_code, 400) #400 Bad request

        #testing by adding invalid closing time
        with self.assertRaises(TypeError):
            status_code = app.create_facility('Swimming pool', 30, 10.00, '8:00:00', '10:0ABC', '63F0DE4724EF6726E1F27D57')
            self.assertEqual(status_code, 400) #400 Bad request

    def test_get_facility(self):
        #testing get facility by name 
        status_code = app.get_facility("Swimming Pool")
        self.assertEqual(status_code, 200)

        #testing get facility by ID
        status_code = app.get_facility("ID")
        self.assertEqual(status_code, 200)

        #testing get facility by invalid ID
        with self.assertRaises(TypeError):
            status_code = app.get_facility("123abc45de")
            self.assertEqual(status_code, 400)

        #testing get facility by non existing name
        #testing get facility by non existing ID 
        #testing get facility by an invalid ID i.e: mix of alphabets and integers


    #def edit_facility_capacity(self):