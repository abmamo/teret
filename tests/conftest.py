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
def test_user(test_app):
    with test_app.app_context():
        # insert user data
        test_user = User.query.filter_by(email=test_app.config["USER_EMAIL"]).first()
        assert test_user is not None
        assert test_user.email == test_app.config["USER_EMAIL"]
        assert test_user.check_password(test_app.config["USER_PASSWORD"])
        assert not test_user.configrmed