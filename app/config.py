# env management
from dotenv import load_dotenv
# load env
load_dotenv()
import os

class Config: 
    # app dir
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATABASE_CONNECT_OPTIONS = {}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # application threads. a common general assumption is
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
    # UPLOADS_DEFAULT_DEST = BASE_DIR + 'app/static/images/'
    UPLOADS_DEFAULT_DEST = "./app/static/images/"
    UPLOADS_DEFAULT_URL = os.environ.get("DOMAIN") + "/static/images/"
    # UPLOADED_IMAGES_DEST = os.path.join(BASE_DIR, '/app/static/images/')
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
    USER_EMAIL = os.environ.get("USER_EMAIL")
    USER_PASSWORD = os.environ.get("USER_PASSWORD")
    # server name
    #SERVER_NAME = os.environ.get("SERVER_NAME")
    DOMAIN = os.environ.get("DOMAIN")

class TestingConfig(Config):
    # db 
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(Config.BASE_DIR, "teret.test.db")
    DEBUG = True
    TESTING = True

class DevelopmentConfig(Config):
    # db 
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(Config.BASE_DIR, "teret.dev.db")
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    # db
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(Config.BASE_DIR, "teret.db")
    DEBUG = False