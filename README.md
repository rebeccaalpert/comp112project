# Comp 112 Final Project

To run, you will need to create a MySQL database. This application uses an unsecured database right now (created as root with no password on localhost).

On the MySQL command line interface, type "CREATE DATABASE development;" and then create a table by typing the following: CREATE TABLE users (
uid INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
firstname VARCHAR(100) NOT NULL,
lastname VARCHAR(100) NOT NULL,
email VARCHAR(120) NOT NULL UNIQUE,
pwdhash VARCHAR(100) NOT NULL
);  

You will also need to create a table for topics as follows: CREATE TABLE topics (uid INT NOT NULL PRIMARY KEY AUTO_INCREMENT, topicname VARCHAR(100) NOT NULL UNIQUE);  

Provision the topics table with a starter value, General, as follows: INSERT INTO topics (uid, topicname) VALUES ('0', 'General');  

You can test to make sure your database is working by going to http://localhost:5000//testdb. 

To run the program:
* source venv/bin/activate
* pip install -r requirements.txt
* python server.py
