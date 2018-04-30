# Comp 112 Final Project

This project is a topic-based chat server that multiple clients can connect to. The server forwards chat messages to clients in the appropriate chatrooms and stores messages in case users switch rooms. There is user authentication, and users can create new topic-based chatrooms.

Users can translate messages into the language of their choice, and privately chat with other users. There is also a user management module: Users can vote to ban users from a chatroom, moderators can unilaterally ban or unban users from a chatroom, and messages are screened based on the likelihood they will be toxic to a conversation.

To run, you will need to create a MySQL database. This application uses an unsecured database right now (created as root with no password on localhost). The database must be called "development."

To create the database (if you already have MySQL installed):
* mysql -u root
* CREATE DATABASE development;
* QUIT

I updated the program to automatically create the tables needed.

For more information on MySQL (including installation), go to https://dev.mysql.com/doc/mysql-getting-started/en/.

You can test to make sure your database is working by going to http://localhost:5000/testdb once the program is running. 

To run the program:
* source venv/bin/activate
* pip install -r requirements.txt
* python server.py
