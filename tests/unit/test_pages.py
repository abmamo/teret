import pytest
from app.mod_auth.models import User


def test_home_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200


def test_about_page(test_client):
    """
    Given a flask application test getting the about page
    """
    response = test_client.get('/about')
    assert response.status_code == 200
