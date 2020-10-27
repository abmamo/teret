import pytest


def test_home_page(test_app):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    # with app context
    with test_app.app_context():
        # expose wekzeug client
        test_client = test_app.test_client()
        response = test_client.get('/')
        assert response.status_code == 200

def test_signin_page(test_app, test_user):
    """
    GIVEN a Flask application
    WHEN the '/signin' page is requested (GET)
    THEN check the response is valid
    """
    # with app context
    with test_app.app_context():
        # expose wekzeug client
        test_client = test_app.test_client()
        response = test_client.get('/signin')
        assert response.status_code == 200
        data = {"email": "major.abenezer@gmail.com", "password": "testpassword"}
        response = test_client.post('/signin', data=data)
        assert response.status_code == 302

def test_forgot_page(test_app):
    """
    GIVEN a Flask application
    WHEN the '/forgot' page is requested (GET)
    THEN check the response is valid
    """
    # with app context
    with test_app.app_context():
        # expose wekzeug client
        test_client = test_app.test_client()
        response = test_client.get('/reset')
        assert response.status_code == 200

def test_nonexistent_page(test_app):
    # with app context
    with test_app.app_context():
        # expose wekzeug client
        test_client = test_app.test_client()
        response = test_client.get('/get')
        assert response.status_code == 404


