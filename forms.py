from flask_wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField, SelectField
from models import db, User, Topic

class TopicForm(Form):
  topicname = TextField("Topic",  [validators.Required("Please enter a topic name.")])
  submit = SubmitField("CREATE CHATROOM")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return False
    
    topic = Topic.query.filter_by(topicname = self.topicname.data.lower()).first()
    if topic:
      self.topicname.errors.append("That topic name is already taken")
      return False
    else:
      return True

class SignupForm(Form):
  firstname = TextField("First name",  [validators.Required("Please enter your first name.")])
  lastname = TextField("Last name",  [validators.Required("Please enter your last name.")])
  language = SelectField('Language', coerce=int)
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  username = TextField("Username",  [validators.Required("Please enter your username.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("CREATE ACCOUNT")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return False
    
    u_email = User.query.filter_by(email = self.email.data.lower()).first()
    u_username = User.query.filter_by(username = self.username.data).first()
    if u_email is None and u_username is None:
        return True
    else:
      self.email.errors.append("That email or username is already taken.")
      return False

class RandomForm(Form):
  interest = TextField("Enter a new interest", [validators.Required("Please enter an interest.")])
  submit = SubmitField("Submit Interest")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return False
    else:
      return True

class ProfileForm(Form):
  firstname = TextField("First name", [validators.Required("Please enter your first name.")])
  lastname = TextField("Last name",  [validators.Required("Please enter your last name.")])
  language = SelectField('Language', coerce=int)
  password = PasswordField('New Password')
  submit = SubmitField("Update Profile")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return False
    else:
      return True

class SigninForm(Form):
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("SIGN IN")
  
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return False
    
    user = User.query.filter_by(email = self.email.data).first()
    if user and user.check_password(self.password.data):
      return True
    else:
      self.email.errors.append("Invalid e-mail or password")
      return False
