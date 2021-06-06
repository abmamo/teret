"""
    models.py: auth bp db models
"""
from datetime import datetime

# import database session
from app.extensions import db


class DateTimeMixin(
    object
):  # pylint: disable=useless-object-inheritance,too-few-public-methods
    """
    timestamp class
    """

    created_on = db.Column(db.DateTime, default=datetime.now)
    updated_on = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class Post(
    DateTimeMixin, db.Model
):  # pylint: disable=useless-object-inheritance,too-few-public-methods
    """
    post class
    """

    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    slug = db.Column(db.String(255))
    content = db.Column(db.Text)
    tags = db.Column(db.String(255))
    image_filename = db.Column(db.String, default=None, nullable=True)
    image_url = db.Column(db.String, default=None, nullable=True)
    published = db.Column(db.Boolean, default=False)
    published_on = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        """
        post string representation method
        """
        return "<Post {}>".format(self.slug)
