# teret [![Actions Status](https://github.com/abmamo/teret/workflows/teret/badge.svg)](https://github.com/abmamo/teret/actions)
blogging engine built using flask + summernotejs + SQLAlchemy + SQLite (or any backend supported by SQLAlchemy).

### quickstart

1. clone the respository and navigate to folder
  ```
    git clone git@github.com:abmamo/teret.git &&
    cd teret
  ```
2. create a virtual environment
  ```
    python3 -m venv env
  ```
3. create .env file
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
