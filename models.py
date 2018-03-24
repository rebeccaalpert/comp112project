from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
  uid = db.Column(db.Integer, primary_key = True)
  firstname = db.Column(db.String(100))
  lastname = db.Column(db.String(100))
  email = db.Column(db.String(120), unique=True)
  pwdhash = db.Column(db.String(128))
  topics = db.relationship('Topic', backref='User', lazy='dynamic')
  messages = db.relationship('Message', backref='User', lazy='dynamic')
  
  def __init__(self, firstname, lastname, email, password, topics, messages):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.email = email.lower()
    self.set_password(password)
    
  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)
  
  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)

class Topic(db.Model):
  uid = db.Column(db.Integer, primary_key = True)
  topicname = db.Column(db.String(100), unique=True)
  user_id = db.Column(db.Integer, db.ForeignKey(User.uid))
  messages = db.relationship('Message', backref='Topic', lazy='dynamic')

  def __init__(self, topicname, user_id):
    self.topicname = topicname.title()
    self.user_id = user_id

class Message(db.Model):
  uid = db.Column(db.Integer, primary_key = True)
  text = db.Column(db.String(4096))
  posted = db.Column(db.DateTime, default = datetime.now)
  user_id = db.Column(db.Integer, db.ForeignKey(User.uid))
  user_email = db.Column(db.String(128))
  topic_id = db.Column(db.Integer, db.ForeignKey(Topic.uid))
  topic_name = db.Column(db.String(100))

  def __init__(self, text, user_id, user_email, topic_id, topic):
    self.text = text
    self.user_id = user_id
    self.user_email = user_email
    self.topic_id = topic_id
    self.topic_name = topic

class PrivateMessage(db.Model):
  uid = db.Column(db.Integer, primary_key = True)
  text = db.Column(db.String(4096))
  posted = db.Column(db.DateTime, default = datetime.now)
  sender_id = db.Column(db.Integer, db.ForeignKey(User.uid))
  sender_email = db.Column(db.String(128))
  receiver_id = db.Column(db.Integer, db.ForeignKey(User.uid))
  receiver_email = db.Column(db.String(128))

  def __init__(self, text, sender_id, sender_email, receiver_id, receiver_email):
    self.text = text
    self.sender_id = sender_id
    self.sender_email = sender_email
    self.receiver_id = receiver_id
    self.receiver_email = receiver_email