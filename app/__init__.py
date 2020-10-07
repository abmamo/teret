# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# import login
from flask_login import LoginManager

# import mail manager
from flask_mail import Mail, Message

# import csrf protections
from flask_wtf.csrf import CSRFProtect, CSRFError

# import serializer for generating tokens
from itsdangerous import URLSafeTimedSerializer

# import image upload plugins
from flask_uploads import UploadSet, IMAGES, configure_uploads

# import config
import app.config as config

# date utils
import babel

# global variables
uploads = None
ts = None


def create_app():
    try:
        # Define the WSGI application object
        app = Flask(__name__)
        # Configurations
        app.config.from_object(config)
        global uploads
        # Configure the image uploading via Flask-Uploads
        uploads = UploadSet("uploads", IMAGES)
        configure_uploads(app, uploads)
        global ts
        # initialize serializer with the app secret key
        ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])
        # import extensions
        from app.extensions import csrf, login, mail, migrate, db

        with app.app_context():
            # init extensions
            # csrf
            csrf.init_app(app)
            # login
            login.init_app(app)
            login.login_view = "auth.signin"
            # mail
            mail.init_app(app)
            # db
            db.init_app(app)
            # migration
            migrate.init_app(app, db)
            # import model
            from app.mod_auth.models import User

            # initialise login manager
            @login.user_loader
            def load_user(id):
                return User.query.get(int(id))

            # Sample HTTP error handling
            @app.errorhandler(400)
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

            @app.errorhandler(404)
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

            @app.errorhandler(500)
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

            @app.errorhandler(502)
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

            @app.errorhandler(CSRFError)
            def handle_csrf_error(e):
                return (
                    render_template("error.html", message=e.description, status_code=400),
                    400,
                )

            # date formatting
            @app.template_filter()
            def format_datetime(value, format="medium"):
                if format == "full":
                    format = "EEEE, d. MMMM y 'at' HH:mm"
                elif format == "medium":
                    format = "EE dd.MM.y HH:mm"
                elif format == "short":
                    format = "MMM d. y"
                return babel.dates.format_datetime(value, format)

            # Import a module / component using its blueprint handler variable (mod_auth)
            from app.mod_auth.controllers import mod_auth as auth_module
            from app.mod_base.controllers import mod_base as base_module
            from app.mod_cms.controllers import mod_cms as cms_module

            # Register blueprint(s)
            app.register_blueprint(auth_module)
            app.register_blueprint(base_module)
            app.register_blueprint(cms_module)
            # create all schema
            db.create_all()
        # return app
        return app
    except Exception as e:
        # log
        current_app.logger.warning("factory failed.")
        # return error page
        abort(500)
