# Comp 112 Final Project

To run, you will need to create a MySQL database. This application uses an unsecured database right now (created as root with no password on localhost).

I updated the program to automatically create the tables needed. There is currently a bug where if you try to run the server multiple times, it will yell at you because the "General" chatroom is in there twice. To get around it until I fix it, just open the MySQL database and type: DROP TABLE message; DROP TABLE topic;  

Then try running the server again. You can test to make sure your database is working by going to http://localhost:5000/testdb. 

New features: 
* When new chatrooms are added, sockets are used to update the list of available chatrooms for everyone
* Topics are stored in the database and are used to populate the list of available chatrooms on refresh
* Users are stored in the database, but I haven't implemented a list of active users yet
* Messages are also stored in the database, but I haven't implemented "back messages" from before you joined the chatroom yet
* There are one-to-many relationships between users and topics, users and messages, and topics and messages. I will use these relationships for showing "back messages"

To run the program:
* source venv/bin/activate
* pip install -r requirements.txt
* python server.py
