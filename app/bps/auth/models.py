"""
    models.py: auth bp db models
"""
# datetime
from datetime import datetime

# hashing
from werkzeug.security import generate_password_hash, check_password_hash

# db user class
from flask_login import UserMixin

# redirect
from flask import url_for

# import mail send function
from app.mail import send_mail

# extensions
from app.extensions import db, ts


class IdMixin(
    object
):  # pylint: disable=useless-object-inheritance,too-few-public-methods
    """
    id generator class
    """

    id = db.Column(db.Integer, primary_key=True)


class DateTimeMixin(
    object
):  # pylint: disable=useless-object-inheritance,too-few-public-methods
    """
    timestamp class
    """

    created_on = db.Column(db.DateTime, default=datetime.now)
    updated_on = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class ConfirmMixin(
    object
):  # pylint: disable=useless-object-inheritance,too-few-public-methods
    """
    confirmation class
    """

    confirmed = db.Column(db.Boolean, default=False)
    confirmed_at = db.Column(db.DateTime, default=datetime.now)


# pylint: disable=useless-object-inheritance,too-few-public-methods
class User(IdMixin, UserMixin, ConfirmMixin, DateTimeMixin, db.Model):
    """
    user class
    """

    __tablename__ = "users"
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(192), nullable=False)
    posts = db.relationship("Post", backref="author", lazy="dynamic")

    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password)

    def set_password(self, password):
        """
        set user password

        params:
            - password: user password
        """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """
        check user password against hash

        params:
            - password: user password
        """
        return check_password_hash(self.password, password)

    def __repr__(self):
        """
        string representation of user
        """
        return "<User {}>".format(self.email)


def register_user(app):
    """
    register app user

    params:
        - app: flask web app instance
    """
    # init extensions with app context
    with app.app_context():
        # create all tables
        db.create_all()
        # create user
        # pylint: disable=bad-option-value
        create_user(app)


def create_user(app):  # pylint: disable=inconsistent-return-statements
    """
    create admin user

    params:
        - app: flask app
        - User: db user model
        - db: sqlalchemy session
    """
    # with app context
    with app.app_context():
        # create user
        # find user
        user = User.query.filter_by(email=app.config["USER_EMAIL"]).first()
        # check email has been found
        if user is not None:
            # check password
            if user.check_password(app.config["USER_PASSWORD"]):
                pass
            else:
                # update password
                user.set_password(app.config["USER_PASSWORD"])
                # save changes
                db.session.commit()
        else:
            # initialize user
            user = User(
                email=app.config["USER_EMAIL"], password=app.config["USER_PASSWORD"]
            )
            # add to session
            db.session.add(user)
            db.session.commit()
            # assert user properly created
            assert user.id is not None
        # disable email confirmation by default (change in config.ppy)
        if app.config["USER_CONFIRMED"]:
            user.confirmed = True
            db.session.add(user)
            db.session.commit()
        else:
            # send confirmation email
            if user.confirmed is False:
                # prepare email
                subject = "confirm account"
                # generate token
                token = ts.dumps(user.email, salt="email-confirm-key")
                # build recover url
                confirm_url = url_for("auth.confirm_email", token=token, _external=True)
                # alert user
                print("account confirmation sent or use link below: ")
                print(confirm_url)
                # send the emails
                send_mail(
                    subject, app.config["MAIL_USERNAME"], [user.email], confirm_url
                )
