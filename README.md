# teret
The word ተረት(teret) in Amharic translates to story. Stories have been an integral part of human existence. They have provided and continue to provide a medium to transfer important social information through time and space. Teret is a platform built to create and manage stories containing rich media such as images, embedded social media links, videos, text, and much more. 

It is built using a tech stack that includes but is not limited to Flask/JavaScript/HTML/CSS/PostgreSQL/Elasticsearch/Jinja/SummernoteJS. It is comprised of three main modules: the user accessible base module, the authentication module, and the content management module. The base module mainly serves published stories and information about the project while the authentication module handles authentication and authorization to access the CMS. This is done through a combination of python decorators and Flask Login. The CMS module is comprised of a dashboard for managing stories and a rich text editor.  

### Quickstart
The application was built using Flask and needs python installed to work. To run the application:

1. Create a virtual environment
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
   
### Technical Overview:

##### Backend

Teret uses the Flask web framework and a combination of SQLAlchemy + PostgreSQL + Elasticsearch to manage users and stories in a database. It can also work with a locally stored SQLite database. 

###### Database

The database is PostgreSQL. This is because SQLite is super light and considering there is going to be a lot of rich content it is not sturdy enough.

Sqlalchemy provides a ORM to modify data easily by creating defined models. There are defined models: post and user.

At the lowest level there is the DBAPI which interacts with the database at the lowest level and is used by the ORM. The engine is a python object which manages connections to the database. Since a database is designed to be accessed by many users at a time the engine controls and manages the database’s resources and DBAPI connections. An engine is created once when an application is initialized and stays alive for the duration of the application. A session is the abstraction layer which represents a series of transactions with a database as well as holds all objects that have not yet been written to the database. A session can be thought of as a staging area. 

The post model allows the modification of stories. It has defined fields of
- Id
- Title
- Slug
- Content
- Tags
- image_filename
- image_url
- Published
- user_id -> relationship

The user model allows the management of users such as authentication and authorization.
- Id
- Email
- password_hash
- Posts -> relationship 

These two models are inherently linked since posts are created and managed by users. I decided this to be a many to many relationship / followed database design

CMS

The cms module uses the flask uploads module in addition to http routes to manage content. There is an asynchronous request made to the server when a user uploads an image since it would be inefficient to store it as a base64 image the image is uploaded to the server temporarily and saved permanently once the post is saved.

The CMS has 5 main methods:
- Save
- Edit
- Publish
- Unpublished
- Delete

All four utilize dynamic routes i.e. save/<id> where id is the id of the post in question. 

Auth

Authentication module utilizes the flask login module in conjunction with SQLAlchemy to manage users. Whenever credentials are provided the email is queried and if it is appropriate (doesn’t already exist in the database for signup or is not a valid email address in the database for signing)

- Signin
- Signup -> what kind of vibe 

Testing

The testing for the application is handled by purest. It follows the design guidelines set by Brian Okken. There is a separation between functional and unit tests. How to test flask apps was another challenge with the lack of online resources.

Frontend

The UI  is fully responsive across devices and follows material design principles. It is built using HTML/CSS/JavaScript/Jinja2. A very neat feature implemented using colortheif.js allows the color palette of a story to match the primary colors of its image to give the reader a richer experience.

The editor uses summer note.js in conjunction with asynchronous Ajax requests to upload rich content. The design follows material design principles.


Challenges:

The Challenge: creating a platform for creating, editing, and manipulating rich text content. Rich text content usually includes text formatting information, images, tables and so on.

The Solution: using a wysiwyg editor that allows you to store the text as a blog in a PostgreSQL database. This solution came short for images as storing images as base64 text files in database affected load times and efficiency adversely. 

The workaround: Added an asynchronous upload event to the editor using JavaScript and Flask that allows the user to upload images and videos to the server and continue on editing without stopping.

### Technical Overview:

#### Backend

Teret uses Flask to serve various application and a combination of SQLAlchemy + PostgreSQL + Elasticsearch to manage users and index stories in a database. It can also work with a locally stored SQLite database for storage.

#### Frontend

The UI  is fully responsive across devices and follows material design principles. It is built using HTML/CSS/JavaScript/Jinja2. A very neat feature implemented using colortheif.js allows the color palette of a story to match the primary colors of its image to give the reader a richer experience.
