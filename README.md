# teret [![Actions Status](https://github.com/abmamo/teret/workflows/teret/badge.svg)](https://github.com/abmamo/teret/actions)
blogging engine built using flask + summernotejs + SQLAlchemy + SQLite/PostgreSQL.

### Quickstart

1. clone the respository and navigate to folder
  ```
    git clone git@github.com:abmamo/teret.git &&
    cd teret
  ```
2. create a virtual environment
  ```
      python3 -m venv env
  ```
2. install dependencies
  ```
      pip install -r requirements.txt
  ```
3. run application
  ```
      python wsgi.py
  ```
4. Head over to http://localhost:5000/auth/signup to create an account. An email will be sent to the account used for signing up. Once you confirm your account you will be redirected to the signin page and once you sign in to the CMS.
