<h2 align="center">🚀 Cogen - CRUD generator for a flask web app</h2>
<br />
COGEN is a code generator for building flask web application. With a given database model,it generates a fully working app with a backend and frontend UI that allows users to create, read, update and delete records on the web. The generated code is clean and easy-to-customize.


## Main App Tech Stack
Frontend: JavaScript, jQuery, AJAX, Jinja2, Bootstrap, HTML5, CSS3
Backend: Python, Flask, PostgreSQL, SQLAlchemy

## Generated App Tech Stack
Frontend: JavaScript, jQuery, AJAX, Jinja2, Bootstrap, HTML5, CSS3
Backend: Python, Flask, PostgreSQL, SQLAlchemy


## Generated App Features
 - PostgreSQL Support
 - User Account
    - Registration
    - Login

 - Landing Page

 - Pages generated for each table
    - List
    - View
    - Add
    - Delete
    - Update

----
## Screenshots

---
## Installation

#### Requirements:
 - Python 3.7
 - PostgreSQL

#### Clone repository
```
$ https://github.com/leizleho/Cogen.git
```

#### Create virtual environment
```
$ python -m venv env
```

#### Activate the environment
```
$ source env/bin/activate
```

#### Install dependencies
```
$ pip install -r requirements.txt
```

#### Create database 'cogen'
```
$ createdb cogen
```
#### Create your database tables and seed🌱sample data
```
$ python -i seed.py
$ seed_data()
```

#### Run the app from the command line
```
$ python server.py
```

#### TODO
 - Complete API module
 - Add react frondend
 - Add Search functionality
 - Export function


### File Structure
<pre>
cogen/
   app/
      mod_api/                     <-- API module
      mod_gen/                     <-- Code generator module
      mod_main/                    <-- Main app pages (Home, About, etc)
      mod_project/                 <-- Project module - used for your app config
      mod_user/                    <-- User Acount, Login, Registration
      models/                      <-- Data model for project/app configurations
      static/
      templates/
   builds/
   env/
   tests/
   .gitignore
   README.md
   requirements.txt
   server.py
   tests.py

</pre>
