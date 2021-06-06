"""
    errors.py: contains functions to render error pages
"""
# flask blueprint
from flask import Blueprint, render_template

# csrf error
from flask_wtf.csrf import CSRFError

errors = Blueprint(
    "errors",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@errors.app_errorhandler(400)
def bad_request(error):
    """
    bad request handler
    """
    # error code
    status_code = 400
    # return error page
    return (
        render_template("error.html", message=str(error), status_code=status_code),
        400,
    )


@errors.app_errorhandler(404)
def not_found(error):
    """
    not found handler
    """
    # error code
    status_code = 404
    # return error page
    return (
        render_template("error.html", message=str(error), status_code=status_code),
        404,
    )


@errors.app_errorhandler(500)
def server_error(error):
    """
    server error handler
    """
    # error code
    status_code = 500
    # return error page
    return (
        render_template("error.html", message=str(error), status_code=status_code),
        500,
    )


@errors.app_errorhandler(502)
def bad_gateway(error):
    """
    bad gateway handler
    """
    # error code
    status_code = 502
    # return error page
    return (
        render_template("error.html", message=str(error), status_code=status_code),
        502,
    )


@errors.app_errorhandler(CSRFError)
def handle_csrf_error(error):
    """
    csrf error handler
    """
    return (
        render_template("error.html", message=error.description, status_code=400),
        400,
    )
