import os
import pytest
from app.factory import create_app
from app.auth.models import User


@pytest.fixture(scope="module")
def test_client():
    # create app
    app = create_app(environment="testing")
    # expose wekzeug client
    testing_client = app.test_client()
    # establish application context
    ctx = app.app_context()
    ctx.push()
    # testing happens
    yield testing_client
    # if test db exists delete
    if os.path.exists(os.path.join(app.config["BASE_DIR"], "teret.test.db")):
        # get base dir
        os.remove(os.path.join(app.config["BASE_DIR"], "teret.test.db"))
    # remove app context
    ctx.pop()


@pytest.fixture(scope="module")
def init_database():
    # create app
    app = create_app()

    with app.app_context():
        from app.extensions import db

        # create database tables
        db.create_all()
        # insert user data
        user_one = User("test_one@test.com", "testonepassword")
        user_two = User("test_two@test.com", "testtwopassword")
        # add users to database
        db.session.add(user_one)
        db.session.add(user_two)
        # commit changes
        db.session.commit()
        # test
        yield db
        # drop all tables created
        db.drop_all()
