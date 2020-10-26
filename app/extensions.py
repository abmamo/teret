# auth
from flask_login import LoginManager

# mail
from flask_mail import Mail, Message

# csrf 
from flask_wtf.csrf import CSRFProtect

# db migration
from flask_migrate import Migrate

# db orm
from flask_sqlalchemy import SQLAlchemy

# logging
import logging
import traceback
# configure logging
logger = logging.getLogger(__name__)

try:
    # init extensions
    # csrf
    csrf = CSRFProtect()
    # auth
    login = LoginManager()
    # mail
    mail = Mail()
    # migration
    migrate = Migrate()
    # db orm
    db = SQLAlchemy()
except Exception as e:
    # log
    logger.warning("init extensions failed with: %s" % str(e))
