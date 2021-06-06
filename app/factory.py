"""
    factory.py: contains function to configure & create flask web app
"""
# app logging
import logging

# dependencies
from flask import Flask

# app extensions
from app.extensions import register_extensions

# app user
from app.bps.auth.models import register_user

# config
from app.config import config_dict

# import blueprints
from app.bps.errors import errors as error_module
from app.bps.macros import macros as macros_module
from app.bps.auth.controllers import auth as auth_module
from app.bps.base.controllers import base as base_module
from app.bps.cms.controllers import cms as cms_module

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
    # register exts.
    register_extensions(app=app)
    # register bps
    app.register_blueprint(error_module)
    app.register_blueprint(macros_module)
    app.register_blueprint(auth_module)
    app.register_blueprint(base_module)
    app.register_blueprint(cms_module)
    # register user
    register_user(app=app)
    # return app
    return app
