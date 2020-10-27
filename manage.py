# app factory
from app.factory import create_app
# db extension
from app.extensions import db
# migration libraries
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
# env
from dotenv import load_dotenv
import os

# load env
load_dotenv()
# get environment
environment = os.environ.get("ENVIRONMENT")
# create app
app = create_app(environment=environment)
# with app context
with app.app_context():
    # init db
    db.init_app(app)
    # init migration manager
    migrate = Migrate(app, db)
    manager = Manager(app)
    # add migration command
    manager.add_command("db", MigrateCommand)

# run migration manager
if __name__ == "__main__":
    manager.run()
