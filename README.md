# Comp 112 Final Project

This project is a topic-based chat server that multiple clients can connect to. The server forwards chat messages to clients in the appropriate chatrooms and stores messages in case users switch rooms. There is user authentication, and users can create new topic-based chatrooms.

To run, you will need to create a MySQL database. This application uses an unsecured database right now (created as root with no password on localhost).

I updated the program to automatically create the tables needed.

You can test to make sure your database is working by going to http://localhost:5000/testdb. 

New features: 
* Topics are stored in the database and are used to populate the list of available chatrooms on refresh
* When new chatrooms are added, sockets are used to update the list of available chatrooms for everyone until they refresh
* When a user creates a new chatroom, they're redirected to the new chatroom
* Messages are stored in the database and users are shown prior messages when they navigate to a channel
* Users are stored in the database and the currently active users for each channel are displayed for each
* When new users join a chatroom, sockets are used to update the list of active users for everyone until they refresh
* If a user tries to access a chatroom that doesn't exist, they're redirected to the general chatroom

To do:
* Chatroom deletion

To run the program:
* source venv/bin/activate
* pip install -r requirements.txt
* python server.py
