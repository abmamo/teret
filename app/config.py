"""
    config.py: contains 3 API configuration classes DevelopmentConfig, TestingConfig,
    & ProductionConfig.

    in addition, it also has a config dict that maps the above 3 classes to a string

    config_dict = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }
"""
# io
import os
import pathlib

# env management
from dotenv import load_dotenv

# load env
load_dotenv()


class Config:  # pylint: disable=too-few-public-methods
    """
    base config object
    """

    # blog name
    APP_NAME = os.getenv("APP_NAME") or "TERET / ተረት"
    # base dir
    BASE_DIR = str(pathlib.Path(__file__).parent.parent.absolute())
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
    UPLOADS_DEFAULT_URL = os.getenv("DOMAIN", "http://127.0.0.1:5000") + "/static/images/"
    # UPLOADED_IMAGES_DEST = os.path.join(BASE_DIR, '/app/static/images/')
    UPLOADS_IMAGES_DEST = "./app/static/images/"
    UPLOADED_IMAGES_URL = os.getenv("DOMAIN", "http://127.0.0.1:5000") + "/static/images/"
    # email configuration
    MAIL_SERVER = os.environ.get("MAIL_SERVER") or ""
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "write@teret.com")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "teret-admin-email")
    # server name
    SERVER_NAME = os.getenv("SERVER_NAME", "http://127.0.0.1:5000")
    SESSION_COOKIE_DOMAIN = os.getenv("SERVER_NAME", "http://127.0.0.1:5000")
    DOMAIN = os.getenv("DOMAIN", "http://127.0.0.1:5000")
    # user has to confirm
    USER_CONFIRMED = True


class TestingConfig(Config):  # pylint: disable=too-few-public-methods
    """
    testing config object
    """

    # db
    DB_URI = "sqlite:///" + os.path.join(Config.BASE_DIR, "teret.test.db")
    DEBUG = False
    TESTING = True
    WTF_CSRF_ENABLED = False
    CSRF_ENABLED = False
    # set max users
    USER_EMAIL = "test@test.com"
    USER_PASSWORD = "testpassword"


class DevelopmentConfig(Config):  # pylint: disable=too-few-public-methods
    """
    dev config object
    """

    # db
    DB_URI = "sqlite:///" + os.path.join(Config.BASE_DIR, "teret.dev.db")
    DEBUG = True
    TESTING = True
    # set max users
    USER_EMAIL = os.environ.get("USER_EMAIL")
    USER_PASSWORD = os.environ.get("USER_PASSWORD")


class ProductionConfig(Config):  # pylint: disable=too-few-public-methods
    """
    prod config object
    """

    # db
    DB_URI = "sqlite:///" + os.path.join(Config.BASE_DIR, "teret.db")
    DEBUG = False
    # set max users
    USER_EMAIL = os.environ.get("USER_EMAIL")
    USER_PASSWORD = os.environ.get("USER_PASSWORD")


# importable config dict that maps each configuration
# class from above to a keyword (can be used to get
# the configuration just using one key word w/o having
# to import all 3 classes i.e. config_dict["development"]
# returns DevelopmentConfig)
config_dict = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
