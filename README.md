# teret
### technical overview
my blogging application built in flask + HTML/CSS/JavaScript. currently using a sqlite database on a digitalocean server to store content but can be integrated and has been tested with PostgreSQL.

can use any rich text editing JavaScript code as the application is modularized and the editor is independent from other parts of the application.

Stylistically the site uses the material design language. It also has an integrated JavaScript music player.

The application backend is built in Flask and uses libraries such as Flask-SQLAlchemy. To install all requirements you can 

1. Create a virtual environment
  ```
      python -m venv env
  ```
2. Install all the requirements recursively
  ```
      pip install -r requirements.txt
  ```
3. Run the application. It will open in your browser at 127.0.0.1
   ```
      python wsgi.py
   ```
### the why

the app was inspired by the urge to chronicle my experiences as an international student and a young coder in Portland. the core vision is sharing real-life stories and experiences to bridgen the gap between the various cultural spaces I have existed in. especially as a computer science major existing in a time where technology has played and plays such a significant role in shaping the world
  
