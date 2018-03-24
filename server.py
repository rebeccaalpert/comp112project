from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import render_template, request, flash, session, url_for, redirect
from forms import SignupForm, SigninForm, TopicForm
from models import db, User, Topic, Message, PrivateMessage
import datetime

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'nuttertools'
socketio = SocketIO(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/development'

db.init_app(app)

#from models import db
#db.init_app(app)

@app.before_first_request
def initialize_database():
	db.create_all()
	missing = Topic.query.filter_by(topicname = 'General').first()
	if missing is None:
		t = Topic('General', None)
		db.session.add(t)
		db.session.commit()

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/testdb')
def testdb():
	if db.session.query("1").from_statement("SELECT 1").all():
		return 'It works.'
	else:
		return 'Something is broken.'

@app.route('/chat', methods=['GET', 'POST'])
def chat():
	form = TopicForm()
	topics = Topic.query.all()
	users = User.query.all()
	messages = Message.query.all()

	session['room'] = 'General'

	if 'email' not in session:
		return redirect(url_for('signin'))

	user = User.query.filter_by(email = session['email']).first()

	if user is None:
		return redirect(url_for('signin'))
	else:
		if request.method == 'POST':
			if form.validate() == False:
				return render_template('chat.html', form=form, topics=topics, users=users, messages=messages)
			else:
				uid = user.uid
				newtopic = Topic(form.topicname.data, uid)
				db.session.add(newtopic)
				db.session.commit()
				session['topic'] = newtopic.topicname
				return redirect('/chat/' + newtopic.topicname)
		
		if request.method == 'GET':
			return render_template('chat.html', form=form, topics=topics, users=users, messages=messages)

@app.route('/chat/<chatroom_title>')
def show_chatroom(chatroom_title):
	form = TopicForm()
	topics = Topic.query.all()
	users = User.query.all()
	messages = Message.query.all()

	topic = Topic.query.filter_by(topicname = chatroom_title).first()

	if topic is None:
		return redirect(url_for('chat'))

	session['room'] = topic.topicname

	if 'email' not in session:
		return redirect(url_for('signin'))

	user = User.query.filter_by(email = session['email']).first()

	if user is None:
		return redirect(url_for('signin'))
	else:
		if request.method == 'POST':
			if form.validate() == False:
				return render_template('chat.html', form=form, topics=topics, users=users, messages=messages)
			else:
				uid = user.uid
				newtopic = Topic(form.topicname.data, uid)
				db.session.add(newtopic)
				db.session.commit()
				session['topic'] = newtopic.topicname
				return redirect('/chat/' + newtopic.topicname)
		
		if request.method == 'GET':
			return render_template('chat.html', form=form, topics=topics, users=users, messages=messages)

@app.route('/private_chat/<username>')
def private_chat(username):
	form = TopicForm()
	topics = Topic.query.all()
	users = User.query.all()
	messages = PrivateMessage.query.all()

	chat_partner = User.query.filter_by(email = username).first()

	if chat_partner is None:
		return redirect(url_for('chat'))

	session['room'] = chat_partner.email

	if 'email' not in session:
		return redirect(url_for('signin'))

	user = User.query.filter_by(email = session['email']).first()

	if user is None:
		return redirect(url_for('signin'))
	else:
		if request.method == 'POST':
			if form.validate() == False:
				return render_template('private.html', form=form, topics=topics, users=users, messages=messages)
			else:
				uid = user.uid
				newtopic = Topic(form.topicname.data, uid)
				db.session.add(newtopic)
				db.session.commit()
				session['topic'] = newtopic.topicname
				return redirect('/chat/' + newtopic.topicname)
		
		if request.method == 'GET':
			return render_template('private.html', form=form, topics=topics, users=users, messages=messages)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupForm()

	session['room'] = 'General'

	if 'email' in session:
		return redirect(url_for('chat')) 
	
	if request.method == 'POST':
		if form.validate() == False:
			return render_template('signup.html', form=form)
		else:
			newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data, None, None)
			db.session.add(newuser)
			db.session.commit()
			session['email'] = newuser.email
			return redirect(url_for('chat'))
	
	if request.method == 'GET':
		return render_template('login.html', form=form)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
	form = SigninForm()

	session['room'] = 'General'

	if 'email' in session:
		return redirect(url_for('chat')) 

	if request.method == 'POST':
		if form.validate() == False:
			return render_template('signin.html', form=form)
		else:
			session['email'] = form.email.data
			return redirect(url_for('chat'))

	elif request.method == 'GET':
		return render_template('signin.html', form=form)

@app.route('/signout')
def signout():
	if 'email' not in session:
		return redirect(url_for('signin'))

	session.pop('email', None)
	session.pop('room', None)
	return redirect(url_for('signin'))

@socketio.on('joined', namespace='/chat')
def joined(message):
	print('message =', message)
	room = message['data']['room']
	session['room'] = room
	join_room(room)
	print(session.get('email'))
	print('has joined')
	emit('status', {'msg': session.get('email') + ' has entered ' + room + '.'}, room=room)

@socketio.on('private_joined', namespace='/private_chat')
def joined(message):
	print('message =', message)
	room = message['data']['room']
	session['room'] = room
	join_room(room)
	print(session.get('email'))
	print('has joined')
	emit('status', {'msg': session.get('email') + ' has entered ' + room + '.'}, room=room)

@socketio.on('message', namespace='/chat')
def chat_message(message):
	print("message = ", message)
	print(message['data']['message'])
	email = session.get('email')
	room = session.get('room')
	emit('message', {'text': message['data']['message'], 'author': email, 'time': ' just now'}, room=room)
	user = User.query.filter_by(email=email).first()
	uid = user.uid
	username = user.email
	room = Topic.query.filter_by(topicname=room).first()
	topic_uid = room.uid
	topic_name = room.topicname
	message = Message(message['data']['message'], uid, username, topic_uid, topic_name)
	db.session.add(message)
	db.session.commit()

@socketio.on('private_message', namespace='/private_chat')
def private_message(message):
	print("message = ", message)
	print(message['data']['message'])
	email = session.get('email')
	room = session.get('room')
	emit('private_message', {'text': message['data']['message'], 'author': email, 'time': ' just now'}, room=room)
	sender = User.query.filter_by(email=email).first()
	sender_id = sender.uid
	sender_email = sender.email
	receiver = User.query.filter_by(email=room).first()
	receiver_id = receiver.uid
	receiver_email = receiver.email
	message = PrivateMessage(message['data']['message'], sender_id, sender_email, receiver_id, receiver_email)
	db.session.add(message)
	db.session.commit()

@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    leave_room(room)
    print(session.get('email'))
    print('left room')
    emit('status', {'msg': session.get('email') + ' has left ' + room + '.'}, room=room)
    session.pop('room', None)

@socketio.on('private_left', namespace='/private_chat')
def left(message):
    room = session.get('room')
    leave_room(room)
    print(session.get('email'))
    print('left room')
    emit('status', {'msg': session.get('email') + ' has left ' + room + '.'}, room=room)
    session.pop('room', None)

@socketio.on('new_topic', namespace='/chat')
def new_topic(message):
	print("New topic\n")
	print(message)
	print(message['data']['room'])
	emit('update_topics', {'msg': { 'room': message['data']['room'] }}, broadcast=True)

if __name__ == '__main__':
	socketio.run(app)
