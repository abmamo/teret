# app factory
from app.factory import create_app
# env
from dotenv import load_dotenv
import os
# load env
load_dotenv()
# get environment
environment = os.environ.get("ENVIRONMENT")
# create app
app = create_app(environment=environment)
# run app
if __name__ == "__main__":
    app.run()
