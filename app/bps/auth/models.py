# datetime
from datetime import datetime

# extensions
from app.extensions import login, db

# hashing
from werkzeug.security import generate_password_hash, check_password_hash
# db user class
from flask_login import UserMixin


class IdMixin(object):
    id = db.Column(db.Integer, primary_key=True)


class DateTimeMixin(object):
    created_on = db.Column(db.DateTime, default=datetime.now)
    updated_on = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class ConfirmMixin(object):
    confirmed = db.Column(db.Boolean, default=False)
    confirmed_at = db.Column(db.DateTime, default=datetime.now)


# Define a base model for other models to inherit
class User(IdMixin, UserMixin, ConfirmMixin, DateTimeMixin, db.Model):
    __tablename__ = "users"
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(192), nullable=False)
    posts = db.relationship("Post", backref="author", lazy="dynamic")

    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<User {}>".format(self.email)


# user loader
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

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
        create_user(app, User, db)


def create_user(app, User, db):
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
        if user != None:
            # check password
            if user.check_password(app.config["USER_PASSWORD"]):
                pass
            else:
                # update password
                user.set_password(app.config["USER_PASSWORD"])
                # save changes
                db.session.commit()
        else:
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
                app.logger.error("user creation failed: %s" % str(e))
                # return
                return None
        # disable email confirmation by default (change in config.ppy)
        if app.config["USER_CONFIRMED"]:
            user.confirmed = True
            db.session.add(user)
            db.session.commit()
        else:
            # send confirmation email
            if user.confirmed == False:
                # import mail send function
                from app.mail import send_mail
                try:
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
                except Exception as e:
                    # log
                    print("send confirmation failed: %s" % str(e))
                    # return error page
                    return None

