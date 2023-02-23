#!flask/bin/python

import os
import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app #, db, models
# from app.models import User, Book
from flask_login import current_user, login_user, logout_user

# The function responsible for setting up and tearing down all the data
# and objects that may be reused in multiple tests
@pytest.fixture
def set_tear_fixture():
    print("Testing the 'set up' / 'tear down' function")
    # 'yield' returns data to whatever function makes use of this fixture
    yield "test string from the fixture function"
    print("End of the 'set up' / 'tear down' function")

# A temporary placeholder function for testing the set up and teardown
# It should always return True
def test_placeholder0(set_tear_fixture):
    app.logger.info(f"Printing the {set_tear_fixture}")
    print(f"Printing the {set_tear_fixture}")
    app.logger.info('asserting True')
    assert True

# A temporary placeholder function for testing the output when 'False' is returned
def test_placeholder1():
    app.logger.error('asserting False')
    assert False
