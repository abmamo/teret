# import factory
from app.factory import create_app

# create app
app = create_app()
# run app
if __name__ == "__main__":
    app.run()
