from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class BannedUser(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.uid'))
  topic_id = db.Column(db.Integer, db.ForeignKey('topic.uid'))
  times_flagged = db.Column(db.Integer)

  def __init__(self, user_id, topic_id):
    self.user_id = user_id
    self.topic_id = topic_id
    self.times_flagged = 0

class Moderator(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.uid'))
  topic_id = db.Column(db.Integer, db.ForeignKey('topic.uid'))

  def __init__(self, user_id, topic_id):
    self.user_id = user_id
    self.topic_id = topic_id

class Language(db.Model):
  uid = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30))
  code = db.Column(db.String(3))

  def __init__(self, name, code):
    self.name = name
    self.code = code

class Cache(db.Model):
  uid = db.Column(db.Integer, primary_key=True)
  source_code = db.Column(db.String(3))
  target_code = db.Column(db.String(3))
  original_text = db.Column(db.String(4096))
  translated_text = db.Column(db.String(4096))
  msg_id = db.Column(db.Integer)
  match = db.Column(db.Integer)

  def __init__(self, source, target, text, translated, msg_id, match):
    self.source_code = source
    self.target_code = target
    self.original_text = text
    self.translated_text = translated
    self.msg_id = msg_id
    self.match = match

class User(db.Model):
  uid = db.Column(db.Integer, primary_key = True)
  firstname = db.Column(db.String(100))
  lastname = db.Column(db.String(100))
  email = db.Column(db.String(120), unique=True)
  pwdhash = db.Column(db.String(128))
  topics = db.relationship('Topic', backref='User', lazy='dynamic')
  messages = db.relationship('Message', backref='User', lazy='dynamic')
  interests = db.relationship('Interest', backref='User', cascade="all, delete-orphan", lazy='dynamic')
  topic_name = db.Column(db.String(100))
  random = db.Column(db.String(120))
  lang = db.Column(db.Integer, db.ForeignKey(Language.uid))
  
  def __init__(self, firstname, lastname, email, password, topics, messages, lang):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.lang = lang
    self.email = email.lower()
    self.random = ""
    self.set_password(password)
    
  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)
  
  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)

class Interest(db.Model):
  uid = db.Column(db.Integer, primary_key = True)
  interest_name = db.Column(db.String(100))
  user_id = db.Column(db.Integer, db.ForeignKey(User.uid))

  def __init__(self, name):
    self.interest_name = name

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
  score = db.Column(db.Integer)

  def __init__(self, text, user_id, user_email, topic_id, topic, score):
    self.text = text
    self.user_id = user_id
    self.user_email = user_email
    self.topic_id = topic_id
    self.topic_name = topic
    self.score = score

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

class RandomMessage(db.Model):
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
