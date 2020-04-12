# teret
The word ተረት(teret) in Amharic translates to story. Stories have been an integral part of human existence. They have provided and continue to provide a medium to transfer important social information. Teret is a platform built to create and manage short stories containing rich media such as images, embedded social media links, videos, text, animations, and so more. 

It is built using a tech stack that includes but is not limited to Flask/JavaScript/HTML/CSS/PostgreSQL/Elasticsearch/Jinja/SummernoteJS. 

### Quickstart
The application was built using Flask and needs python3 installed to work. To run the application:

1. Clone the respository and navigate to folder
  ```
    git clone git@github.com:abmamo/teret.git &&
    cd teret
  ```
2. Create a virtual environment 
  ```
      python3 -m venv env
  ```
2. Install all the requirements listed in the requirements file
  ```
      pip install -r requirements.txt
  ```
3. Run the application. It will open in your browser at 127.0.0.1
  ```
      python wsgi.py
  ```
4. Head over to http://localhost:5000/auth/signup to create an account. An email will be sent to the account used for signing up. Once you confirm your account you will be redirected to the signin page and afterwards to the CMS/editor.
   
### Technical Overview

##### Backend

Teret is built using the Flask web framework. It uses Flask Blueprints to divide the application into three main blueprints/modules: the user accessible base module, the authentication module, and the content management module. The base module mainly serves published stories and information about the project. The authentication module handles account creation and recovery methods whilc the CMS module provides a simple dashboard to edit, publish, unpublish, and delete stories.

###### Database

The database used in production is PostgreSQL but the application can also run with a locally stored SQLite database. This can be changed in the config.py
```
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'teret.db')
```

SQLAlchemy provides a ORM to modify data easily from this database by creating defined models. The two models in use here are the post and user models.

The post model allows the modification of stories. It has defined fields of
- id -> unique identifier
- title -> title of story
- slug -> url friendly slug of the title
- content -> rich blob content of the story
- tags -> tag of each story
- image_filename -> filename for primary image to be displayed on card
- image_url -> url for primary image to be displayed on card
- published -> boolean value 
- user_id -> relationship

The user model allows the management of users such as authentication and authorization.
- id -> unique identifier for users
- email -> email associated with account
- password_hash -> sha256 hash of the users password
- posts -> relationship 

These two models are inherently linked since posts are created and managed by users. I decided this to be a many to many relationship / followed database design

###### CMS

The CMS module uses the Flask Uploads module in conjunction with the database to manage stories. Stories are created using a HTML form initialized with summernote.js editor. The majority of the rich text editing capabilities are handled through summernote. However, since by default summernote stores all uploaded images as a base64 image, I had to implement an asynchronuous uploader that returns the URL of the uploaded image.

The CMS has 5 main methods:

- Save
- Edit
- Publish
- Unpublished
- Delete

All four utilize dynamic Flask routes i.e. save/<id> where id is the id of the post in question. 

###### Auth

The authentication module utilizes Flask Login to manage user sessions and the database to store user information. It has 5 primary methods: 

- signup
- signin
- signout
- reset
- confirm

The signup method allows users to register themselves. There is a variable MAX_USERS_NOT_REACHED in the application configuration that currently limits the number of users signing up. If this is unwanted it can be removed by deleting the
```
app.config['MAX_USERS_NOT_REACHED'] = False
```
line in the controllers.py of the auth module.

Once a user signs up an account, a short lived unique confirmation email is sent to the email address associated with their account. This is done using the itsdangerous module which generates a short lived token by doing
```
token = ts.dumps(email, salt='salt-key')
```
Once a user confirms the email address associated with their account they are redirected to the signin method. The authentication module utilizes Flask Login in conjunction with SQLAlchemy to manage users. Using python decorators, Flask Login allows us to protect routes that need authorization by doing
```
@login_required
app.route('/cms')
```
for instance.

The reset method works similarly to the email confirmation in that it generates a short lived token and sends it to the email address of the user who then has to use that link to access the password change page.

###### Testing

The testing for the application is handled by pytest. The tests are located in the tests directory and are divided into two main parts: unit tests and procedural test. The unit tests test individual functions while functional tests test procedures such as logging in and loggin out. To run tests:
```
python -m pytests --cov tests/
```
Currently working on setting up Travis-CLI integration and writing more tests.

##### Frontend

The UI is fully responsive across devices and follows material design principles. It is built using HTML/CSS/JavaScript/Jinja2. Each story is presented as a material card which opens a modal when clicked which contains the contents of the story. There is a colorthief plugin that matches the navbar to the primary color of the primary story image.

### Challenges

Challenge: creating a platform for creating, editing, and manipulating rich text content. Rich text content usually includes text formatting information, images, tables and so on.

Current Solution: using a wysiwyg editor that allows you to store the text as a blog in a PostgreSQL database. This solution came short for images as storing images as base64 text files in database affected load times and efficiency adversely. 

The Workaround: Added an asynchronous upload event to the editor using JavaScript and Flask that allows the user to upload images and videos to the server and continue on editing without stopping.
