<h2 align="center">🚀 Cogen - CRUD generator for a flask web app</h2>
<br />
COGEN is a code generator for building flask web application. With a given database model,it generates a fully working app with a backend and frontend UI that allows users to create, read, update and delete records on the web. The generated code is clean and easy-to-customize.

## Cogen App Tech Stack

Frontend: JavaScript, jQuery, AJAX, Jinja2, Bootstrap, HTML5, CSS3
Backend: Python, Flask, MSSQL Server/PostgreSQL, SQLAlchemy

## Generated Apps Tech Stack

Frontend: JavaScript, jQuery, AJAX, Jinja2, Bootstrap, HTML5, CSS3
Backend: Python, Flask, MSSQL Server/PostgreSQL, SQLAlchemy

## Generated App Features

- MSSQL Server/PostgreSQL Support
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
 
 
## Screencast at YouTube
[![Screencast at YouTube](https://img.youtube.com/vi/IXnfVXoKiaE/0.jpg)](https://www.youtube.com/watch?v=IXnfVXoKiaE)

----



### Create Project

![](create-project.gif)

### Generate Codes

![](generate-codes.gif)

---

#### Requirements

- Python 3.7
- PostgreSQL or
- MSSQL Server

## Installation

```bash
# Clone repository
$ https://github.com/higorvaz/Python-App-Generator.git


# Create virtual environment
$ python3 -m venv env


# Activate the environment
$ source env/bin/activate


# Install dependencies
$ pip install -r requirements.txt

# Install uwsgi
$ sudo apt install uwsgi-plugin-python3 uwsgi-core


# Create database 'CogenDB'
$ sqlcmd -S localhost -U sa
$ CREATE DATABASE CogenDB
 GO



# Create your database tables and seed🌱sample data
$ python3 -i seed.py
$ seed_data()
```

#### Run the app from the command line

```bash
python3 server.py
```

#### Create ini file to run the main app and the generated app side by side

```text
# Create "main_app.ini" in this directory: "uwsgi/vassals/"
# add the following script and change the chdir path:

[uwsgi]
chdir=/path/to/your/cloned/app
http=:5555
wsgi-file=server.py
callable=app
processes=2
threads=1


# Create "emperor.ini" in this directory: "uwsgi/"
# add the following script and change the emperor path:

[uwsgi]
emperor = /path/to/your/uwsgi/vassals
die-on-term = true

```

#### Run uwsgi emperor to run the main app and the generated app side by side

```bash
uwsgi uwsgi/emperor.ini
```

#### TODO

- Project Database parameter
- Database existing tables read
-- sqlacodegen mssql+pymssql://sa:StrongPa55#@localhost/SampleDB > SampleDB.py
It will create SampleDB.py in your current directory containing all Model Classes code(a pirce of cake 🍰)
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
