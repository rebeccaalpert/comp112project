# Comp 112 Final Project

To run, you will need to create a MySQL database for user login/logout. This application uses an unsecured database right now (created as root with no password).

On the MySQL command line interface, type "CREATE DATABASE development;" and then create a table by typing the following:  
CREATE TABLE users (
uid INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
firstname VARCHAR(100) NOT NULL,
lastname VARCHAR(100) NOT NULL,
email VARCHAR(120) NOT NULL UNIQUE,
pwdhash VARCHAR(100) NOT NULL
);  

To run the program:
* source venv/bin/activate
* pip install -r requirements.txt
* python server.py
