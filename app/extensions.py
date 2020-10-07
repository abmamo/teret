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
    csrf = CSRFProtect()
    login = LoginManager()
    mail = Mail()
    migrate = Migrate()
    db = SQLAlchemy()
except Exception as e:
    # log
    logger.warning("init extensions failed.")
    logger.warning(str(e))
    logger.warning(traceback.print_exc())
