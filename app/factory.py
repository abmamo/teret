"""
    factory.py: contains function to configure & create flask web app
"""
# app logging
import logging

# dependencies
from flask import Flask

# app extensions
from app.extensions import register_extensions

# app blueprints
from app.bps import register_blueprints

# app user
from app.bps.auth.models import register_user

# config
from app.config import config_dict

# configure logger
logging.basicConfig(
    filename="teret.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
)


def create_app(environment="development"):
    """
    create web app

    params:
        - environment: current environment

    """
    # web wsgi app object
    app = Flask(__name__)
    # config here
    app.config.from_object(config_dict[environment])
    # register extendions
    register_extensions(app=app)
    # register blueprints
    register_blueprints(app=app)
    # register user
    register_user(app=app)
    # return app
    return app
