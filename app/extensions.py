# import login
from flask_login import LoginManager

# import mail manager
from flask_mail import Mail, Message

# import csrf protections
from flask_wtf.csrf import CSRFProtect

# import db migration plugins
from flask_migrate import Migrate

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# init extensions
csrf = CSRFProtect()
login = LoginManager()
mail = Mail()
migrate = Migrate()
db = SQLAlchemy()