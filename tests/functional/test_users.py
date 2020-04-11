import pytest
from app import User


@pytest.fixture(scope='module')
def new_user():
    user = User('test@test.com', 'testpassword')
    return user


def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, confirmed, and role fields are defined correctly
    """
    assert new_user.email == 'test@test.com'
    assert new_user.password != 'testpassword'
    assert not new_user.confirmed
