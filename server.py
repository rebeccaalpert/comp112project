from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import render_template, request, flash, session, url_for, redirect
from forms import SignupForm, SigninForm, TopicForm
from models import db, User, Topic, Message, PrivateMessage, Language
import datetime
import math

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'nuttertools'
socketio = SocketIO(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/development'

db.init_app(app)

@app.before_first_request
def initialize_database():
	db.create_all()
	missing = Topic.query.filter_by(topicname = 'General').first()
	if missing is None:
		t = Topic('General', None)
		db.session.add(t)
		db.session.commit()

	langs = Language.query.filter_by(code = 'mn').first()
	
	if langs is None:
		t = Language('Azerbaijan', 'az')
		db.session.add(t)
		t = Language('Malayalam', 'ml')
		db.session.add(t)
		t = Language('Albanian', 'sq')
		db.session.add(t)
		t = Language('Maltese', 'mt')
		db.session.add(t)
		t = Language('Amharic', 'am')
		db.session.add(t)
		t = Language('Macedonian', 'mk')
		db.session.add(t)
		t = Language('English', 'en')
		db.session.add(t)
		t = Language('Maori', 'mi')
		db.session.add(t)
		t = Language('Arabic', 'ar')
		db.session.add(t)
		t = Language('Marathi', 'mr')
		db.session.add(t)
		t = Language('Armenian', 'hy')
		db.session.add(t)
		t = Language('Mari', 'mhr')
		db.session.add(t)
		t = Language('Afrikaans', 'af')
		db.session.add(t)
		t = Language('Mongolian', 'mn')
		db.session.add(t)
		t = Language('Basque', 'eu')
		db.session.add(t)
		t = Language('German', 'de')
		db.session.add(t)
		t = Language('Bashkir', 'ba')
		db.session.add(t)
		t = Language('Nepali', 'ne')
		db.session.add(t)
		t = Language('Belarusian', 'be')
		db.session.add(t)
		t = Language('Norwegian', 'no')
		db.session.add(t)
		t = Language('Bengali', 'bn')
		db.session.add(t)
		t = Language('Punjabi', 'pa')
		db.session.add(t)
		t = Language('Burmese', 'my')
		db.session.add(t)
		t = Language('Papiamento', 'pap')
		db.session.add(t)
		t = Language('Bulgarian', 'bg')
		db.session.add(t)
		t = Language('Persian', 'fa')
		db.session.add(t)
		t = Language('Bosnian', 'bs')
		db.session.add(t)
		t = Language('Polish', 'pl')
		db.session.add(t)
		t = Language('Welsh', 'cy')
		db.session.add(t)
		t = Language('Portuguese', 'pt')
		db.session.add(t)
		t = Language('Hungarian', 'hu')
		db.session.add(t)
		t = Language('Romanian', 'ro')
		db.session.add(t)
		t = Language('Vietnamese', 'vi')
		db.session.add(t)
		t = Language('Russian', 'ru')
		db.session.add(t)
		t = Language('Creole', 'ht')
		db.session.add(t)
		t = Language('Cebuano', 'ceb')
		db.session.add(t)
		t = Language('Galician', 'gl')
		db.session.add(t)
		t = Language('Serbian', 'sr')
		db.session.add(t)
		t = Language('Dutch', 'nl')
		db.session.add(t)
		t = Language('Sinhala', 'si')
		db.session.add(t)
		t = Language('Hill Mari', 'mrj')
		db.session.add(t)
		t = Language('Slovakian', 'sk')
		db.session.add(t)
		t = Language('Greek', 'el')
		db.session.add(t)
		t = Language('Slovenian', 'sl')
		db.session.add(t)
		t = Language('Georgian', 'ka')
		db.session.add(t)
		t = Language('Swahili', 'sw')
		db.session.add(t)
		t = Language('Gujarati', 'gu')
		db.session.add(t)
		t = Language('Sundanese', 'su')
		db.session.add(t)
		t = Language('Danish', 'da')
		db.session.add(t)
		t = Language('Tajik', 'tg')
		db.session.add(t)
		t = Language('Hebrew', 'he')
		db.session.add(t)
		t = Language('Thai', 'th')
		db.session.add(t)
		t = Language('Yiddish', 'yi')
		db.session.add(t)
		t = Language('Tagalog', 'tl')
		db.session.add(t)
		t = Language('Indonesian', 'id')
		db.session.add(t)
		t = Language('Tamil', 'ta')
		db.session.add(t)
		t = Language('Irish', 'ga')
		db.session.add(t)
		t = Language('Tatar', 'tt')
		db.session.add(t)
		t = Language('Italian', 'it')
		db.session.add(t)
		t = Language('Telugu', 'te')
		db.session.add(t)
		t = Language('Icelandic', 'is')
		db.session.add(t)
		t = Language('Turkish', 'tr')
		db.session.add(t)
		t = Language('Spanish', 'es')
		db.session.add(t)
		t = Language('Udmurt', 'udm')
		db.session.add(t)
		t = Language('Kazakh', 'kk')
		db.session.add(t)
		t = Language('Uzbek', 'uz')
		db.session.add(t)
		t = Language('Kannada', 'kn')
		db.session.add(t)
		t = Language('Ukrainian', 'uk')
		db.session.add(t)
		t = Language('Catalan', 'ca')
		db.session.add(t)
		t = Language('Urdu', 'ur')
		db.session.add(t)
		t = Language('Kyrgyz', 'ky')
		db.session.add(t)
		t = Language('Finnish', 'fi')
		db.session.add(t)
		t = Language('Chinese', 'zh')
		db.session.add(t)
		t = Language('French', 'fr')
		db.session.add(t)
		t = Language('Korean', 'ko')
		db.session.add(t)
		t = Language('Hindi', 'hi')
		db.session.add(t)
		t = Language('Xhosa', 'xh')
		db.session.add(t)
		t = Language('Croatian', 'hr')
		db.session.add(t)
		t = Language('Khmer', 'km')
		db.session.add(t)
		t = Language('Czech', 'cs')
		db.session.add(t)
		t = Language('Laotian', 'lo')
		db.session.add(t)
		t = Language('Swedish', 'sv')
		db.session.add(t)
		t = Language('Latin', 'la')
		db.session.add(t)
		t = Language('Scottish', 'gd')
		db.session.add(t)
		t = Language('Latvian', 'lv')
		db.session.add(t)
		t = Language('Estonian', 'et')
		db.session.add(t)
		t = Language('Lithuanian', 'lt')
		db.session.add(t)
		t = Language('Esperanto', 'eo')
		db.session.add(t)
		t = Language('Luxembourgish', 'lb')
		db.session.add(t)
		t = Language('Javanese', 'jv')
		db.session.add(t)
		t = Language('Malagasy', 'mg')
		db.session.add(t)
		t = Language('Japanese', 'ja')
		db.session.add(t)
		t = Language('Malay', 'ms')
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
		session['uid'] = user.uid
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

def convertToNumber (s):
    return int.from_bytes(s.encode(), 'little')

def convertFromNumber (n):
    return n.to_bytes(math.ceil(n.bit_length() / 8), 'little').decode()

@app.route('/private_chat/<username>')
def private_chat(username):
	form = TopicForm()
	topics = Topic.query.all()
	users = User.query.all()
	messages = PrivateMessage.query.all()

	chat_partner = User.query.filter_by(email = username).first()

	if chat_partner is None:
		return redirect(url_for('chat'))

	session['room'] = convertToNumber(chat_partner.email) + convertToNumber(session['email'])
	session['private'] = chat_partner.email

	if 'email' not in session:
		return redirect(url_for('signin'))

	user = User.query.filter_by(email = session['email']).first()

	if user is None:
		return redirect(url_for('signin'))
	else:
		if request.method == 'POST':
			if form.validate() == False:
				return render_template('private.html', form=form, topics=topics, users=users, messages=messages, private=chat_partner.email)
			else:
				uid = user.uid
				newtopic = Topic(form.topicname.data, uid)
				db.session.add(newtopic)
				db.session.commit()
				session['topic'] = newtopic.topicname
				return redirect('/chat/' + newtopic.topicname)
		
		if request.method == 'GET':
			return render_template('private.html', form=form, topics=topics, users=users, messages=messages, private=chat_partner.email)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupForm()

	session['room'] = 'General'

	lang = Language.query.filter_by()
	form.language.choices = [(g.uid, g.name) for g in Language.query.order_by('name')]
	
	if 'email' in session:
		return redirect(url_for('chat')) 
	
	if request.method == 'POST':
		if form.validate() == False:
			return render_template('signup.html', form=form)
		else:
			newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data, None, None, form.language.data)
			db.session.add(newuser)
			db.session.commit()
			session['email'] = newuser.email
			return redirect(url_for('chat'))
	
	if request.method == 'GET':
		return render_template('signup.html', form=form)

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


@app.route('/user_language/<email>', methods=['GET', 'POST'])
def resolveUserLanguage(email):
	if 'email' not in session:
		return redirect(url_for('signin'))

	user = User.query.filter_by(email = email).first()

	if user is None:
		return redirect(url_for('signin'))
	else:
		lang = Language.query.filter_by(uid = user.lang).first()
		if lang:
			return lang.code
		return "-1"

@socketio.on('joined', namespace='/chat')
def joined(message):
	print('message =', message)
	room = message['data']['room']
	session['room'] = room
	join_room(room)
	print(session.get('email'))
	print('has joined')
	emit('status', {'user': session.get('email'), 'msg': session.get('email') + ' has entered ' + room + '.'}, room=room)
	user = User.query.filter_by(email=session.get('email')).first()
	user.topic_name = room
	print(user.topic_name)
	print(session['room'])
	db.session.commit()

@socketio.on('private_joined', namespace='/private_chat')
def joined(message):
	print('message =', message)
	room = message['data']['room']
	session['room'] = room
	join_room(room)
	print(session.get('email'))
	print('has joined')
	emit('private_status', {'msg': session.get('email') + ' is connected.'}, room=room)

@socketio.on('message', namespace='/chat')
def chat_message(message):
	print("message = ", message)
	print(message['data']['message'])
	email = session.get('email')
	room = session.get('room')
	user = User.query.filter_by(email=email).first()
	uid = user.uid
	emit('message', {'text': message['data']['message'], 'author': email, 'time': ' just now'}, room=room)
	username = user.email
	room = Topic.query.filter_by(topicname=room).first()
	topic_uid = room.uid
	topic_name = room.topicname
	msg = Message(message['data']['message'], uid, username, topic_uid, topic_name)
	db.session.add(msg)
	db.session.flush()
	db.session.refresh(msg)
	db.session.commit()


@socketio.on('private_message', namespace='/private_chat')
def private_message(message):
	print("message = ", message)
	print(message['data']['message'])
	email = session.get('email')
	room = session.get('room')
	receiver_email = session.get('private')
	emit('private_message', {'text': message['data']['message'], 'author': email, 'time': ' just now'}, room=room)
	sender = User.query.filter_by(email=email).first()
	sender_id = sender.uid
	sender_email = sender.email
	receiver = User.query.filter_by(email=receiver_email).first()
	receiver_id = receiver.uid
	message = PrivateMessage(message['data']['message'], sender_id, sender_email, receiver_id, receiver_email)
	db.session.add(message)
	db.session.commit()

@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    leave_room(room)
    print(session.get('email'))
    print('left room')
    emit('status', {'user': session.get('email'), 'msg': session.get('email') + ' has left ' + room + '.'}, room=room)
    user = User.query.filter_by(email=session.get('email')).first()
    session.pop('room', None)
    user.topic_name = None
    db.session.commit()

@socketio.on('private_left', namespace='/private_chat')
def left(message):
    room = session.get('room')
    leave_room(room)
    print(session.get('email'))
    print('left room')
    emit('private_status', {'msg': session.get('email') + ' is offline.'}, room=room)
    session.pop('room', None)

@socketio.on('new_topic', namespace='/chat')
def new_topic(message):
	print("New topic\n")
	print(message)
	print(message['data']['room'])
	emit('update_topics', {'msg': { 'room': message['data']['room'] }}, broadcast=True)


@socketio.on('delete_my_chatroom', namespace='/chat')
def delete_my_chatroom(message):
	print("delete_my_chatroom\n")
	print("This is message ")
	print(message)
	id = message['data']['id']
	parent = message['data']['parent']
	topic = Topic.query.filter_by(uid=id).delete()
	db.session.commit()
	emit('delete_my_chatroom', {'msg': parent}, broadcast=True)

if __name__ == '__main__':
	socketio.run(app)
