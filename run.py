from flashcard import app


# from flask import Flask, jsonify, request
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
# from flask_marshmallow import Marshmallow, fields
# from flask_bcrypt import Bcrypt

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# db = SQLAlchemy(app)

# ma = Marshmallow(app)
# bcrypt = Bcrypt(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), index=True, unique=True)
#     email = db.Column(db.String(120), index=True, unique=True)
#     password_hash = db.Column(db.String(128))
#     decks = db.relationship('Deck', backref='author', lazy='dynamic')

#     def __repr__(self):
#         return '<User {}, {}, >'.format(self.username, self.email)

# class Deck(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(140))
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     questions = db.relationship('Question', backref='deck', lazy='dynamic')

#     def __repr__(self):
#         return '<Deck {}>'.format(self.name)


# class Question(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.String(240))
#     answer = db.Column(db.String(240))
#     deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'))

#     def __repr__(self):
#         return '<question {}>'.format(self.body)

# class UserSchema(ma.ModelSchema):
# 	class Meta:
# 		model = User

# class DeckSchema(ma.ModelSchema):
# 	class Meta:
# 		model = Deck

# class QuestionSchema(ma.ModelSchema):
# 	class Meta:
# 		model = Question


# from models import User, Deck, Question

# # @app.route('/register', methods=['POST'])
# # def register_user():
	
# # 	data = request.get_json()
# # 	user = db.session.query(User).filter_by(email=args['email']).first()

# # 	if user:
# # 		return jsonify({'message':'User already exists.'})

# # 	hashed_password = bcrypt.generate_password_hash(data['password_hash']).decode('utf-8')
# # 	new_user = User(username=data['username'], email=data['email'], password_hash=hashed_password)
# # 	db.session.add(new_user)
# # 	db.session.commit()

# # 	return jsonify({'message': 'New user created'})

# @app.route('/login', methods=['POST'])
# def login_user():

# 	data = request.get_json()

# 	hashed_password = bcrypt.generate_password_hash(data['password_hash']).decode('utf-8')
# 	new_user = User(username=data['username'], email=data['email'], password_hash=hashed_password)
# 	db.session.add(new_user)
# 	db.session.commit()
# 	return jsonify({'message': 'New user created'})

# @app.route('/')
# def index():
# 	return jsonify({'in': 'home page'})

# # GET all users
# @app.route('/users')
# def get_users():
# 	users = User.query.all()
# 	user_schema = UserSchema(many=True)
# 	output = user_schema.dump(users).data
# 	return jsonify({'users': output})

# # # POST new user
# # @app.route('/users', method=['POST'])
# # def get_user():
# # 	username = request.get_json('username')
# # 	password = request.get_json('password')
# # 	email = request.get_json('email')
# # 	user_schema = UserSchema(many=True)
# # 	output = user_schema.dump(users).data
# # 	return jsonify({'users': output})


# # GET a specific user
# @app.route('/users/<user_id>')
# def get_user(user_id):
# 	user = User.query.get(user_id)
# 	user_schema = UserSchema()
# 	# deck_schema = deckSchema(many=True)
# 	# output = user_schema.dump(users).data
# 	return user_schema.jsonify(user)

# # GET all decks
# @app.route('/users/<user_id>/decks')
# def get_decks(user_id):
# 	decks = db.session.query(Deck).join(Deck.author).filter(User.id==user_id).all()
# 	deck_schema = DeckSchema(many=True)
# 	output = deck_schema.dump(decks).data
# 	return deck_schema.jsonify(decks)

# # POST a new deck
# @app.route('/users/<user_id>/decks', methods=['POST'])
# def create_deck(user_id):
# 	data = request.get_json()

# 	new_deck = Deck(name=data['name'], author=User.query.get(user_id))
# 	db.session.add(new_deck)
# 	db.session.commit()
# 	return jsonify({'message':'Created a new deck'})


# # GET a individual deck
# @app.route('/users/<user_id>/decks/<deck_id>')
# def get_deck(user_id, deck_id):
# 	deck = db.session.query(Deck).join(Deck.author).filter(Deck.id==deck_id).filter(User.id==user_id).first()
# 	deck_schema = DeckSchema()
# 	output = deck_schema.dump(deck).data
# 	return jsonify({'deck {}'.format(deck.id): output})

# # GET all questions
# @app.route('/users/<user_id>/decks/<deck_id>/questions')
# def get_questions(user_id, deck_id):
# 	questions = db.session.query(Question).join(Question.deck).join(Deck.author).filter(Deck.id==deck_id).filter(User.id==user_id).all()
# 	question_schema = QuestionSchema(many=True)
# 	output = question_schema.dump(questions).data
# 	return jsonify({'questions': output})

# # GET a single question
# @app.route('/users/<user_id>/decks/<deck_id>/questions/<question_id>')
# def get_question(user_id, deck_id, question_id):
# 	question = db.session.query(Question).join(Question.deck).filter(Deck.id==deck_id).filter(Question.id==question_id).first()
# 	question_schema = QuestionSchema()
# 	output = question_schema.dump(question).data
# 	return jsonify({'question {}'.format(question_id): output})

# # POST a new question
# @app.route('/decks/<deck_id>/questions', methods=['POST'])
# def create_question(deck_id):
# 	data = request.get_json()

# 	new_question = Question(body=data['body'], answer=data['answer'], deck=Deck.query.get(deck_id))
# 	db.session.add(new_question)
# 	db.session.commit()
# 	return jsonify({'message':'Created a new question'})

# # This kinda works
# @app.route('/decks/<deck_id>/questions/<question_id>')
# def test(deck_id, question_id):
# 	question = db.session.query(Question).join(Question.deck).filter(Deck.id==deck_id).filter(Question.id==question_id).first()
# 	question_schema = QuestionSchema()
# 	output = question_schema.dump(question).data
# 	return jsonify({'question {}'.format(question_id): output})


if __name__ == "__main__":
	app.run(debug=True)




