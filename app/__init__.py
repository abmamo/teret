# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# import login
from flask_login import LoginManager

# import csrf protections
from flask_wtf.csrf import CSRFProtect, CSRFError

# import image upload plugins
from flask_uploads import UploadSet, IMAGES, configure_uploads

# Define the WSGI application object
app = Flask(__name__)

# initialize csrf protection
csrf = CSRFProtect(app)

# define login manager
login = LoginManager(app)
login.login_view = 'auth.signin'

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Configure the image uploading via Flask-Uploads
images = UploadSet('photos', IMAGES)
configure_uploads(app, images)


# import model
from app.mod_auth.models import User

# initialise login manager
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('400.html', reason=e.description), 400

# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_auth.controllers import mod_auth as auth_module
from app.mod_base.controllers import mod_base as base_module
from app.mod_cms.controllers import mod_cms as cms_module

# Register blueprint(s)
app.register_blueprint(auth_module)
app.register_blueprint(base_module)
app.register_blueprint(cms_module)

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
