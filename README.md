# teret

The word ተረት(tenet) in Amharic translates to story. Stories have been an integral part of human existence and civilizations. They have provided and continue to provide a medium to transfer important survival and social information through time and space. In addition stories can serve as a communication device and a bridge between different cultures. Teret therefore is a platform built to create and manage stories with rich media such as images, embedded social media links, videos, text, and much more. It was inspired by the desire to chronicle my experiences as an international student in Portland and minority in tech. 

Teret is a responsive web application built to create and manage rich text content. It is built using a tech stack that includes but is not limited to Flask/JavaScript/HTML/CSS/PostgreSQL/Elasticsearch/Jinja/SummernoteJS. It is comprised of three main modules: the user accessible base module, the authentication module, and the content management module. The base module mainly serves published stories and information about the project while the authentication module handles authentication and authorization to access the CMS. This is done through a combination of python decorators and Flask Login. The CMS module is comprised of a dashboard for managing stories and a rich text editor. 

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

#### Backend

Teret uses Flask to serve various application and a combination of SQLAlchemy + PostgreSQL + Elasticsearch to manage users and index stories in a database. It can also work with a locally stored SQLite database for storage.

#### Frontend

The UI  is fully responsive across devices and follows material design principles. It is built using HTML/CSS/JavaScript/Jinja2. A very neat feature implemented using colortheif.js allows the color palette of a story to match the primary colors of its image to give the reader a richer experience.
