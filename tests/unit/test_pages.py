import pytest


def test_home_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200

def test_signin_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/signin' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/signin')
    assert response.status_code == 200

def test_forgot_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/forgot' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/reset')
    assert response.status_code == 200

def test_nonexistent_page(test_client):
    response = test_client.get('/get')
    assert response.status_code == 404

