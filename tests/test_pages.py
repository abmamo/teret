"""
    test_pages.py: test page availability
"""


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
        response = test_client.get("/")
        assert response.status_code == 200


def test_signin_page(test_app):
    """
    GIVEN a Flask application
    WHEN the '/signin' page is requested (GET)
    THEN check the response is valid
    """
    # with app context
    with test_app.app_context():
        # expose wekzeug client
        test_client = test_app.test_client()
        response = test_client.get("/signin")
        assert response.status_code == 200
        data = {
            "email": test_app.config["USER_EMAIL"],
            "password": test_app.config["USER_PASSWORD"],
        }
        response = test_client.post("/signin", data=data)
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
        response = test_client.get("/reset")
        assert response.status_code == 200
        data = {"email": test_app.config["USER_EMAIL"]}
        response = test_client.get("/reset", data=data)
        assert response.status_code == 200


def test_nonexistent_page(test_app):
    """
    GIVEN a Flask application
    WHEN the '/reset' page is requested (GET) & (POST)
    THEN check the response is valid
    """
    # with app context
    with test_app.app_context():
        # expose wekzeug client
        test_client = test_app.test_client()
        response = test_client.get("/get")
        assert response.status_code == 302
