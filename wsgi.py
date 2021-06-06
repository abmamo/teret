"""
    wsgi.py: app entry point
"""
# os
import os

# env manager
from dotenv import load_dotenv

# app factory/creation function
from app.factory import create_app

# load env vars
load_dotenv()
# create app
app = create_app(
    # get environment or use development as default
    environment=os.environ.get("ENVIRONMENT", "development")
)

# if executed as script (in dev / testing)
if __name__ == "__main__":
    # run app
    app.run(host=os.environ.get("HOST", "0.0.0.0"), port=int(os.environ.get("PORT", 5000)))
