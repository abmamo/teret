import os
import pytest
from app.factory import create_app
from app.auth.models import User

@pytest.fixture(scope="module")
def test_app():
    # create app
    app = create_app(environment="testing")
    # yield test app
    yield app
    # if test db exists delete
    if os.path.exists(os.path.join(app.config["BASE_DIR"], "teret.test.db")):
        # get base dir
        os.remove(os.path.join(app.config["BASE_DIR"], "teret.test.db"))


@pytest.fixture(scope="module")
def test_db(test_app):
    # with app context
    with test_app.app_context():
        # import db extension
        from app.extensions import db as test_db
        # create database tables
        test_db.create_all()
        # yield session
        yield test_db
        # drop all tables created
        test_db.drop_all()

@pytest.fixture(scope="module")
def test_user(test_db):
    # insert user data
    test_user = User("test_one@test.com", "testonepassword")
    # add users to database
    test_db.session.add(test_user)
    # commit changes
    test_db.session.commit()
    # yield
    yield test_user
    # delete user
    test_db.session.delete(test_user)
    # save changes
    # commit changes
    test_db.session.commit()