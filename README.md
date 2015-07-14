# Item Catalog

---

## Introduction

This is Project 3 for Udacity's Full Stack Web Developer Nanodegree.

Main objectives of this project:

* Develop a RESTful application using the Python framework Flask that provides a list of items within a variety of categories
* Provide a user login and authentication system using a third-party OAuth provider (Google+ in this case)
* Logged-in users have the ability to create, edit and delete their own items

## Requirements

You will need these installed in your computer:

* [Python 2.x](https://www.python.org/downloads/)
* [Flask](http://flask.pocoo.org/)
* [SQLAlchemy](http://www.sqlalchemy.org/download.html)
* [oauth2client](https://github.com/google/oauth2client)
* [httplib2](https://github.com/jcgregorio/httplib2)
* [requests](http://docs.python-requests.org/en/latest/user/install/#install)
* [SQLite](https://www.sqlite.org/download.html)

## Files

These are the files that come with this project:

* **application.py:** This is the main server-side python Flask file which contains the RESTful API for interacting with a SQLite database using SQLAlchemy.

* **client_secrets.json:** This contains info (e.g. client secrets, client id) of a registered app with Google+

* **templates/\*.html** These are the Jinja2 template files which are used by Flask to serve HTML pages

* **db/categoryitems.db** A SQLite database with some test data. If you do not wish to use the test data provided, you can delete this file manually and then create an empty database using `db_setup.py` (please see "Running The Project" below)

* **db/db_setup.py** Creates an empty database

* **db/db\_populate\_test\_data.py** Populates some test data in the database. Note that all existing data will be wiped out during this process.

* **db/db\_show\_all\_data.py** Prints out all data in the database for a quick check of its contents

* **static/css/styles.css** Some basic styles

## Running The Project

* Clone the repository

This respository comes with a default database `db/categoryitems.db` that has some test data. If you do not wish to use it, delete it manually and follow the four steps below:

* In a command shell, cd into the `db` folder:

		> cd db

* Create an empty database:

		> python db_setup.py

* Populate the database with some test data:

		> python db_populate_test_data.py

	or run your own SQLAlchemy python commands to populate the database.

* Cd back to the base directory:

		> cd ..

Now that the database is in place, we can run the application:

* In a command shell, start the server:

		> python application.py

* Open a new browser window and go to url [http://localhost:5000](http://localhost:5000)
