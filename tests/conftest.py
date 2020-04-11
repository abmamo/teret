import pytest
from app import app, db
from app.mod_auth import User


@pytest.fixture(scope='module')
def test_client():
    # expose wekzeug client
    testing_client = app.test_client()
    # establish application context
    ctx = app.app_context()
    ctx.push()
    # testing happens
    yield testing_client

    ctx.pop()


@pytest.fixture(scope='module')
def init_database():
    # create database tables
    db.create_all()
    # insert user data
    user_one = User('test_one@test.com', 'testonepassword')
    user_two = User('test_two@test.com', 'testtwopassword')
    # add users to database
    db.session.add(user_one)
    db.session.add(user_two)
    # commit changes
    db.session.commit()
    # test
    yield db
    # drop all tables created
    db.drop_all()
