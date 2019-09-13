from flashcard import app, db, ma, bcrypt, jwt
from flask import jsonify, request
from flashcard.models import User, Deck, Question
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

class UserSchema(ma.ModelSchema):
	class Meta:
		model = User

class DeckSchema(ma.ModelSchema):
	class Meta:
		model = Deck

class QuestionSchema(ma.ModelSchema):
	class Meta:
		model = Question

@app.route('/register', methods=['POST'])
def register_user():
	data = request.get_json()
	user = db.session.query(User).filter_by(email=data['email']).first()
	if user:
		# 409 conflict, when a resource already exists
		return jsonify({'message':'User already exists.'}), 409
	hashed_password = bcrypt.generate_password_hash(data['password_hash']).decode('utf-8')
	new_user = User(username=data['username'], email=data['email'], password_hash=hashed_password)
	db.session.add(new_user)
	db.session.commit()
	return jsonify({'message': 'New user created'}), 200

@app.route('/login', methods=['POST'])
def login_user():
	data = request.get_json()
	email = data['email']
	password = data['password_hash']

	user = db.session.query(User).filter_by(email=email).first()
	if not user:
		return jsonify({'message':'User with {} does not exist.'.format(email)}), 404
	if bcrypt.check_password_hash(user.password_hash, password):
		access_token = create_access_token(identity=user.id)
		return jsonify(access_token=access_token), 200
	else:
		return jsonify({'message':'Invalid login.'}), 401

@app.route('/')
def index():
	return jsonify({'test': 'home page'})

# GET all users
@app.route('/users')
def get_users():
	users = User.query.all()
	user_schema = UserSchema(many=True)
	output = user_schema.dump(users).data
	return jsonify({'users': output})

# GET a specific user
@app.route('/users/<user_id>')
@jwt_required
def get_user(user_id):
	current_user = get_jwt_identity()
	if current_user == int(user_id):
		user = User.query.get(user_id)
		user_schema = UserSchema()
		return user_schema.jsonify(user), 200
	else:
		return jsonify({'message':'Incorrect user'}), 401

# Test /protected route
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    if current_user:
        return jsonify(logged_in_as=current_user), 200
    else:
    	return jsonify({'message':'Incorrect user'}), 200

# GET all decks
@app.route('/decks', methods=['GET'])
@jwt_required
def get_decks():
	current_user = get_jwt_identity()
	decks = db.session.query(Deck).join(Deck.author).filter(User.id==current_user).all()
	if current_user:
		# decks = db.session.query(Deck).join(Deck.author).filter(User.id==current_user).all()
		deck_schema = DeckSchema(many=True)
		output = deck_schema.dump(decks).data
		return deck_schema.jsonify(decks)
	else:
		return jsonify({'message':'Unauthorized access'})

# GET an individual deck
@app.route('/decks/<deck_id>', methods=['GET'])
@jwt_required
def get_deck(deck_id):
	current_user = get_jwt_identity()
	deck = db.session.query(Deck).join(Deck.author).filter(Deck.id==deck_id).filter(User.id==current_user).first()
	if current_user:
		try:
			deck_schema = DeckSchema()
			question_schema = QuestionSchema(many=True)
			questions = deck.questions.all()
			output = deck_schema.dump(deck).data
			return jsonify({'deck {}'.format(deck.id): output})
		except Exception as e:
			return jsonify({'message':'Unauthorized access'})
	else:
		return jsonify({'message':'Unauthorized access'})

# Create a new deck
@app.route('/decks', methods=['POST'])
@jwt_required
def create_deck():
	current_user = get_jwt_identity()
	data = request.get_json()
	if current_user == int(data["user_id"]):
		new_deck = Deck(name=data['name'], author=User.query.get(current_user))
		db.session.add(new_deck)
		db.session.commit()
		return jsonify({'message':'Created a new deck'}), 200
	else:
		return jsonify({'message':'Unauthorized access'}), 401

# Delete an existing deck
@app.route('/decks/<deck_id>', methods=['POST'])
@jwt_required
def delete_deck(deck_id):
	current_user = get_jwt_identity()
	data = request.get_json()
	if current_user:
		try:
			deck = db.session.query(Deck).filter(Deck.id==deck_id).filter(Deck.user_id==current_user).filter(User.id==current_user).first()
			db.session.delete(deck)
			db.session.commit()
			return jsonify({'message':'Deleted deck'}), 200
		except Exception as e:
			return jsonify({'message':'Unauthorized access'}), 401
	else:
		return jsonify({'message':'Unauthorized access'}), 401

@app.route('/decks/<deck_id>', methods=['PUT'])
@jwt_required
def update_deck_title(deck_id):
	current_user = get_jwt_identity()
	data = request.get_json()
	if current_user:
		try:
			print(data)
			deck = db.session.query(Deck).join(Deck.author).filter(Deck.id==deck_id).filter(User.id==current_user).first()
			deck.name = data['name']
			db.session.commit()
			return jsonify({'message':'Updated Deck title'}), 200
		except Exception as e:
			return jsonify({'message':'No data provided'}), 401
	# Not working properly atm
	else:
		return jsonify({'message':'Unauthorized access'}), 401



			# return redirec("/decks/" + str(deck_id))

# # GET all questions
# @app.route('/users/<user_id>/decks/<deck_id>/questions')
# @jwt_required
# def get_questions(user_id, deck_id):
# 	current_user = get_jwt_identity()
# 	if current_user == int(user_id):
# 		try:
# 			questions = db.session.query(Question).join(Question.deck).filter(Deck.id==deck_id).filter(User.id==current_user).all()
# 			question_schema = QuestionSchema(many=True)
# 			output = question_schema.dump(questions).data
# 			return jsonify({'questions': output})
# 		except Exception as e:
# 			return jsonify({'message':'Unauthorized access'})
# # 	else:
# 		return jsonify({'message':'Unauthorized access'})

# GET all questions
@app.route('/questions', methods=['GET'])
@jwt_required
def get_questions():
	current_user = get_jwt_identity()
	user_query = request.args['q']
	deck = db.session.query(Deck).filter(Deck.id == user_query, Deck.user_id == current_user).first()
	if current_user:
		try:
			questions = deck.questions.all()
			question_schema = QuestionSchema(many=True)
			output = question_schema.dump(questions).data
			return jsonify({'All questions': output})
		except Exception as e:
			return jsonify({'message':'Unauthorized access'})

# GET a single question
# /questions/id?q=deck_id
@app.route('/questions/<question_id>', methods=['GET'])
@jwt_required
def get_question(question_id):	
	current_user = get_jwt_identity()
	user_query = request.args['q']
	if current_user:
		try:
			question = db.session.query(Question).join(Deck).filter(Deck.id == user_query, Question.id == question_id).first()
			question_schema = QuestionSchema()	
			output = question_schema.dump(question).data
			return jsonify({'questions': output})
		except Exception as e:
			return jsonify({'message':'Unauthorized access'})

# Currently is not protecting other routes
@app.route('/decks/<deck_id>/questions/<question_id>', methods=['GET'])
@jwt_required
def get_question_2(deck_id, question_id):	
	current_user = get_jwt_identity()
	# user_query = request.args['q']
	if current_user:
		try:
			question = db.session.query(Question).join(Deck).filter(Deck.id == deck_id, Question.id == question_id).first()
			question_schema = QuestionSchema()	
			output = question_schema.dump(question).data
			return jsonify({'questions': output})
		except Exception as e:
			return jsonify({'message':'Unauthorized access'})


# PUT a single question
# /questions/id?q=deck_id
@app.route('/questions/<question_id>', methods=['PUT'])
@jwt_required
def update_question(question_id):	
	current_user = get_jwt_identity()
	user_query = request.args['q']
	data = request.get_json()
	if current_user:
		question = db.session.query(Question).join(Deck).filter(Deck.id == user_query, Question.id == question_id).first()
		if 'body' in data and question != None:
			question.body =data['body']
		if 'answer' in data and question != None:
			question.answer = data['answer']
		question_schema = QuestionSchema()	
		output = question_schema.dump(question).data
		return jsonify({'questions': output})
	else:
		return jsonify({'message':'Unauthorized access'})

# POST a new question
@app.route('/decks/<deck_id>/questions', methods=['POST'])
def create_question(deck_id):
	data = request.get_json()
	new_question = Question(body=data['body'], answer=data['answer'], deck=Deck.query.get(deck_id))
	db.session.add(new_question)
	db.session.commit()
	return jsonify({'message':'Created a new question'})

# Delete a single question
# /questions/id?q=deck_id
@app.route('/questions/<question_id>', methods=['POST'])
@jwt_required
def delete_question(question_id):	
	current_user = get_jwt_identity()
	user_query = request.args['q']
	if current_user:
		try:
			question = db.session.query(Question).join(Deck).filter(Deck.id == user_query, Question.id == question_id).first()
			db.session.delete(question)
			db.session.commit()
			return jsonify({'message': 'Question deleted'})
		except Exception as e:
			return jsonify({'message':'Unauthorized access'})

