# flask blueprint
from flask import Blueprint
# csrf error
from flask_wtf.csrf import CSRFError

errors = Blueprint('errors',
               __name__,
               template_folder='templates',
               static_folder='static',)
               

@errors.app_errorhandler(400)
def not_found(error):
    # error code
    status_code = 400
    # message
    message = "bad request."
    # return error page
    return (
        render_template("error.html", message=message, status_code=status_code),
        400,
    )

@errors.app_errorhandler(404)
def not_found(error):
    # error code
    status_code = 404
    # message
    message = "resource not found."
    # return error page
    return (
        render_template("error.html", message=message, status_code=status_code),
        404,
    )

@errors.app_errorhandler(500)
def server_error(error):
    # error code
    status_code = 500
    # message
    message = "internal server error."
    # return error page
    return (
        render_template("error.html", message=message, status_code=status_code),
        500,
    )

@errors.app_errorhandler(502)
def server_error(error):
    # error code
    status_code = 502
    # message
    message = "bad gateway."
    # return error page
    return (
        render_template("error.html", message=message, status_code=status_code),
        502,
    )

@errors.app_errorhandler(CSRFError)
def handle_csrf_error(e):
    return (
        render_template("error.html", message=e.description, status_code=400),
        400,
    )