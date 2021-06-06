"""
    conftest.py: contains all pytest configurations & fixtures for testing
"""
import os
import pytest

# app deps
from app.extensions import db
from app.factory import create_app
from app.bps.auth.models import User


@pytest.fixture(scope="module")
def test_app():
    """
    test app fixture
    """
    # create app
    app = create_app(environment="testing")
    app.config["TESTING"] = True
    # yield test app
    yield app
    # if test db exists delete
    if os.path.exists(os.path.join(app.config["BASE_DIR"], "teret.test.db")):
        # get base dir
        os.remove(os.path.join(app.config["BASE_DIR"], "teret.test.db"))


@pytest.fixture(scope="module")
def test_db(test_app):  # pylint: disable=redefined-outer-name
    """
    test db fixture
    """
    # with app context
    with test_app.app_context():
        # create database tables
        db.create_all()
        # yield session
        yield db
        # drop all tables created
        db.drop_all()


@pytest.fixture(scope="module")
def test_user(test_app):  # pylint: disable=redefined-outer-name
    """
    test user fixture
    """
    with test_app.app_context():
        # insert user data
        user = User.query.filter_by(email=test_app.config["USER_EMAIL"]).first()
        assert user is not None
        assert user.email == test_app.config["USER_EMAIL"]
        assert user.check_password(test_app.config["USER_PASSWORD"])
        assert not user.confirmed
