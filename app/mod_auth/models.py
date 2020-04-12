from datetime import datetime
# import database and login manager from application
from app import db, login
# import hashing and hash checking functions
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# define flask login user loader by id
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128),  nullable=False, unique=True)
    password = db.Column(db.String(192),  nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
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
