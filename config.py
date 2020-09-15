# env management
from dotenv import load_dotenv
# load env
load_dotenv()
# Statement for enabling the development environment
import os
DEBUG = True
# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'teret.db')
DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_TRACK_MODIFICATIONS = False
# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2
# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True
# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = os.urandom(256)
# Secret key for signing cookies
SECRET_KEY = os.urandom(256)
# Uploads
#UPLOADS_DEFAULT_DEST = BASE_DIR + 'app/static/images/'
UPLOADS_DEFAULT_DEST = "./app/static/images/"
UPLOADS_DEFAULT_URL = os.environ.get("DOMAIN") + "/static/images/"
#UPLOADED_IMAGES_DEST = os.path.join(BASE_DIR, '/app/static/images/')
UPLOADS_IMAGES_DEST = "./app/static/images/"
UPLOADED_IMAGES_URL = os.environ.get("DOMAIN") + "/static/images/"
# email configuration
MAIL_SERVER = os.environ.get("MAIL_SERVER")
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
# set max users
MAX_USERS_NOT_REACHED = True
