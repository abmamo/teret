"""
    extensions.py: init flask extensions
"""
# logging
import logging

# auth
from flask_login import LoginManager

# mail
from flask_mail import Mail

# csrf
from flask_wtf.csrf import CSRFProtect

# db migration
from flask_migrate import Migrate

# db orm
from flask_sqlalchemy import SQLAlchemy

# uploads
from flask_uploads import UploadSet, IMAGES, configure_uploads

# serializer for generating tokens
from itsdangerous import URLSafeTimedSerializer

# configure logging
logger = logging.getLogger(__name__)

# init extensions
# csrf
csrf = CSRFProtect()
# auth
login = LoginManager()
# mail
mail = Mail()
# migration
migrate = Migrate()
# db orm
db = SQLAlchemy()
# initialize serializer with the app secret key
# pylint: disable=invalid-name
ts = None
# uploads
# pylint: disable=invalid-name
uploads = None


def register_extensions(app):
    """
    register flask extensions

    params:
        - app: Flask WSGI instance
        - environment: env. currently in use
    """
    # log
    logger.debug("registering extensions")
    # set db uri
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config["DB_URI"]
    # log
    logger.debug("register: sqlalchemy")
    # register db_orm orm
    db.init_app(app)
    # log
    logger.debug("register: migration")
    # register migration
    # log
    logger.debug("register: login manager")
    # register login manager
    login.init_app(app)
    login.login_view = "auth.signin"
    login.login_message = "please sign in"
    # log
    logger.debug("register: csrf")
    # csrf
    csrf.init_app(app)
    # log
    logger.debug("register: mail")
    # mail
    mail.init_app(app)
    # log
    logger.debug("register: ts")
    # serializer
    global ts  # pylint: disable=global-statement
    ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    # log
    logger.debug("register: uploads")
    # get global variable upload
    global uploads  # pylint: disable=global-statement
    # configure the image uploading via Flask-Uploads
    uploads = UploadSet("uploads", IMAGES)
    configure_uploads(app, uploads)
