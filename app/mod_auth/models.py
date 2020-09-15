from datetime import datetime
# import database and login manager from application
from app.extensions import login
from app.extensions import db
# import hashing and hash checking functions
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# define flask login user loader by id
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

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
    __tablename__ = 'users'
    email = db.Column(db.String(128),  nullable=False, unique=True)
    password = db.Column(db.String(192),  nullable=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.email)
