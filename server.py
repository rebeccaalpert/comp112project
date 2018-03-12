from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import render_template, request, flash, session, url_for, redirect
from forms import SignupForm, SigninForm, TopicForm
from models import db, User, Topic

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'nuttertools'
socketio = SocketIO(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/development'

from models import db
db.init_app(app)

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

	if 'email' not in session:
		return redirect(url_for('signin'))

	user = User.query.filter_by(email = session['email']).first()

	if user is None:
		return redirect(url_for('signin'))
	else:
		if request.method == 'POST':
			if form.validate() == False:
				return render_template('chat.html', form=form, topics=topics)
			else:
				newtopic = Topic(form.topicname.data)
				db.session.add(newtopic)
				db.session.commit()
				session['topic'] = newtopic.topicname
				return redirect(url_for('chat'))
		
		if request.method == 'GET':
			return render_template('chat.html', form=form, topics=topics)

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
			newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
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

@socketio.on('message', namespace='/chat')
def chat_message(message):
	print("message = ", message)
	print(message['data']['message'])
	print(session.get('email'))
	room = session.get('room')
	emit('message', {'msg': session.get('email') + ':' + message['data']['message']}, room=room)

# not currently implemented
@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    leave_room(room)
    print(session.get('email'))
    print('left room')
    emit('status', {'msg': session.get('email') + ' has left ' + room + '.'}, room=room)
    session.pop('room', None)

if __name__ == '__main__':
	socketio.run(app)
