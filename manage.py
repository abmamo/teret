# import factory
from app.factory import create_app
# import db extension
from app.extensions import db
# migration scripts
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
# env
from dotenv import load_dotenv
import os
import sys

# load env
load_dotenv()
# get environment
environment = os.environ.get("ENVIRONMENT")
# create app
app = create_app(environment=environment)
with app.app_context():
    db.init_app(app)
    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command("db", MigrateCommand)
# run app
if __name__ == "__main__":
    manager.run()
