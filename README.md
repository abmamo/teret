# teret [![test](https://github.com/abmamo/teret/actions/workflows/test.yaml/badge.svg?branch=master)](https://github.com/abmamo/teret/actions/workflows/test.yaml) [![deploy](https://github.com/abmamo/teret/actions/workflows/deploy.yml/badge.svg?branch=master)](https://github.com/abmamo/teret/actions/workflows/deploy.yml)
blogging application with a WYSIWYG editor built using Flask + SummernoteJS + SQLite (or any other relational database supported by SQLAlchemy)

### quickstart

1. clone the respository and navigate to folder
  ```
    git clone https://github.com/abmamo/teret.git &&
    cd teret
  ```
2. create a virtual environment
  ```
    python3 -m venv env
  ```
3. create .env file (this is where configuration variables will be stored for the app such as app name, log in info)
  ```
    mv .env.sample .env
  ```
  then edit .env to make sure configurations are not placeholder values
4. install dependencies
  ```
    pip install -r requirements.txt
  ```
3. run application
  ```
      python wsgi.py
  ```
4. head over to http://127.0.0.1:5000 to get started. An account will be created from config variables in .env
