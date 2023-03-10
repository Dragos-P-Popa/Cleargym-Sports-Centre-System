import pytest
from app import app, db

# The fixture configuration and tests are split into separate files
# and kept within a designated 'tests' folder,
# as recommended by the pytest documentation:
# https://docs.pytest.org/en/7.1.x/explanation/goodpractices.html

############################# SET UP AND TEAR DOWN #############################

# The function responsible for setting up and tearing down all the data
# and objects that may be reused in multiple tests
@pytest.fixture
def app_fixture():

    app.logger.info("Start of the 'set up' / 'tear down' function")

    app.config.from_object('config')
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    # Setting up temporary database tables in memory
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    # Create the tables
    db.create_all()

    # 'yield' returns the app's test instance to whatever function
    # makes use of this fixture
    yield app.test_client()

    # Delete the tables
    db.drop_all()

    app.logger.info("End of the 'set up' / 'tear down' function")


# Show the app instance returned by the app_fixture() function
def test_fixture_setup(app_fixture):
    app.logger.info(f"The app_fixture() function returns {app_fixture}")
    assert True
