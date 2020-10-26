# Import flask and template operators
from flask import Flask, render_template, abort, url_for

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# import login
from flask_login import LoginManager

# import mail manager
from flask_mail import Mail, Message

# import csrf protections
from flask_wtf.csrf import CSRFProtect

# import serializer for generating tokens
from itsdangerous import URLSafeTimedSerializer

# import image upload plugins
from flask_uploads import UploadSet, IMAGES, configure_uploads

# import config
import app.config as config

# sys
import sys

# global variables
uploads = None
ts = None


def create_app():
        #try:
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
            from app.auth.models import User

            # initialise login manager
            @login.user_loader
            def load_user(id):
                return User.query.get(int(id))

            # import blueprints
            from app.errors import errors as error_module
            from app.macros import macros as macros_module
            from app.auth.controllers import auth as auth_module
            from app.base.controllers import base as base_module
            from app.cms.controllers import cms as cms_module

            # register blueprint(s)
            app.register_blueprint(error_module)
            app.register_blueprint(macros_module)
            app.register_blueprint(auth_module)
            app.register_blueprint(base_module)
            app.register_blueprint(cms_module)
            # create all schema
            db.create_all()
            # create user
            try:
                # find user
                user = User.query.filter_by(email=app.config["USER_EMAIL"]).first()
                # check email has been found
                if user != None:
                    # delete userc
                    db.session.delete(user)
                    # save 
                    db.session.commit()
            except Exception as e:
                # log
                print("deleting existing user failed: %s" % str(e))
                # return
                return None
            try:
                # initialize user
                user = User(email=app.config["USER_EMAIL"], password=app.config["USER_PASSWORD"])
                # add to session
                db.session.add(user)
                db.session.commit()
                assert user.id is not None
                db.session.close()
            except Exception as e:
                # log
                print("user init failed: %s" % str(e))
                # return
                return None
            """
            from app.mail import send_mail
            try:
                # prepare email
                subject = "confirm account"
                # generate token
                token = ts.dumps(app.config["USER_EMAIL"], salt="email-confirm-key")
                # build recover url
                confirm_url = url_for("auth.confirm_email", token=token, _external=True)
                # send the emails
                send_mail(
                    subject, app.config["MAIL_USERNAME"], [app.config["USER_EMAIL"]], confirm_url
                )
            except Exception as e:
                # log
                print("send confirmation failed: %s" % str(e))
                # return error page
                return None
            """
        # return app
        return app
        #except Exception as e:
        # log
        #print("factory failed.")
        #print(str(e))
        # exit
        #sys.exit(1)