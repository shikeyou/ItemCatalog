# Item Catalog

---

## Introduction

This is Project 3 for Udacity's Full Stack Web Developer Nanodegree.

Main objectives of this project:

* Develop a RESTful application using the Python framework Flask that provides a list of items within a variety of categories, including a 
* Provide a JSON endpoint for users to query all data in the database
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

* **application.py:** This is the main server-side python Flask file which contains the RESTful API for interacting with a SQLite database using SQLAlchemy. It contains all necessary routes to handle different URL requests, as well as a JSON endpoint (`/catalog.json`) which contains all the data in the database in JSON format.

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

Next, we will need to register a Google+ app and download the client secrets json file.

* Go to [https://console.developers.google.com](https://console.developers.google.com) and login using your Google account

* Click on the Create Project button. A New Project dialog should appear.

* Give the project a suitable name (e.g. Item Catalog App). Project ID can be left as default. Once you are done, click on the Create button.

*  On the left sidebar, click on APIs & Auth > Credentials.

*  In the main area, click on the Create New Client ID button. A  Create Client ID dialog should appear.

* Select Web Application, then click on the Configure Consent Screen button. The dialog should close.

* In the Consent Screen page, put in at least an email address and a product name. Click on the Save button. The dialog should close.

* In the Create Client ID page, add `http://localhost:5000` to the Authorized JavaScript Origins text box. Then click on the Create Client ID button. You have now successfully create a new project.

* Copy the Client ID. Open up `templates/\login.html` using a text editor and paste the client id into the `data-clientid` field. 

* Click on the Download JSON button to download a .json file which contains client info such as client ID and client secret. Rename this file to `client_secrets.json` and place it in the base folder together with `application.py`.

Now that all the necessary things are in place, we can run the application:

* In a command shell, start the server:

		> python application.py

* Open a new browser window and go to url [http://localhost:5000](http://localhost:5000)
