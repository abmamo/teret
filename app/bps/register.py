"""
    register.py: contains a single function to
                 iteratively register individual bps

    blueprints
        - pages - publicly accessible pages bp
        - errors - error handler pages bp
"""
# logging
import logging

# import blueprints
from app.bps.errors import errors as error_module
from app.bps.macros import macros as macros_module
from app.bps.auth.controllers import auth as auth_module
from app.bps.base.controllers import base as base_module
from app.bps.cms.controllers import cms as cms_module

# init logger
logger = logging.getLogger(__name__)


def register_blueprints(app):
    """
    register blueprints to flask app

    params:
        - app: Flask app we are registering blueprints with
    """
    # log
    logger.debug("registering blueprints")
    # register blueprint(s)
    app.register_blueprint(error_module)
    app.register_blueprint(macros_module)
    app.register_blueprint(auth_module)
    app.register_blueprint(base_module)
    app.register_blueprint(cms_module)
