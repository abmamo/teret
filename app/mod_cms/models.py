from app import db

class Post(db.Model):
     __tablename__ = 'posts'
     id = db.Column(db.Integer, primary_key=True)
     title = db.Column(db.String(255))
     slug = db.Column(db.String(255))
     content = db.Column(db.Text)
     tags = db.Column(db.String(255))
     image_filename = db.Column(db.String, default=None, nullable=True)
     image_url = db.Column(db.String, default=None, nullable=True)
     published = db.Column(db.Boolean, default=False)
     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


     def __repr__(self):
         return '<Post {}>'.format(self.slug)
