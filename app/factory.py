# dependencies
from flask import Flask, render_template, abort, url_for

# orm
from flask_sqlalchemy import SQLAlchemy

# login manager
from flask_login import LoginManager

# mail
from flask_mail import Mail, Message

# csrf
from flask_wtf.csrf import CSRFProtect

# serializer for generating tokens
from itsdangerous import URLSafeTimedSerializer

# uploads
from flask_uploads import UploadSet, IMAGES, configure_uploads

# config
import app.config as config

# logging
import logging

# global variables
# uploading
uploads = None
# timed serializer
ts = None

logging.basicConfig(filename="teret.log",
                    level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")

def create_app(environment="development"):
    try:
        # wsgi app object
        app = Flask(__name__)
        # configuration
        if environment == "production":
            # production
            app.config.from_object(config.ProductionConfig)
        elif environment == "testing":
            # testing
            app.config.from_object(config.TestingConfig)
        else:
            # dev
            app.config.from_object(config.DevelopmentConfig)
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
            login.login_message = "please sign in"
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
            # create all tables
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
                # assert user properly created
                assert user.id is not None
            except Exception as e:
                # log
                print("user init failed: %s" % str(e))
                # return
                return None
            # import mail send function
            from app.mail import send_mail
            try:
                # prepare email
                subject = "confirm account"
                # generate token
                token = ts.dumps(app.config["USER_EMAIL"], salt="email-confirm-key")
                # build recover url
                confirm_url = url_for("auth.confirm_email", token=token, _external=True)
                print("account confirmation sent or use link below: ")
                print(confirm_url)
                # send the emails
                send_mail(
                    subject, app.config["MAIL_USERNAME"], [app.config["USER_EMAIL"]], confirm_url
                )
            except Exception as e:
                # log
                print("send confirmation failed: %s" % str(e))
                # return error page
                return None
        # return app
        return app
    except Exception as e:
        # log
        print("factory failed with: %s" % str(e))
        # return failure
        return None