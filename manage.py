# import factory
from app import create_app
from app.extensions import db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# create app
app = create_app()
with app.app_context():
    db.init_app(app)
    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command("db", MigrateCommand)
# run app
if __name__ == "__main__":
    manager.run()
