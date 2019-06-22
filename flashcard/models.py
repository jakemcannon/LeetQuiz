from flashcard import db, ma
from flask import jsonify, request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow, fields

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    decks = db.relationship('Deck', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}, {}, >'.format(self.username, self.email)

class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    questions = db.relationship('Question', backref='deck', lazy='dynamic')

    def __repr__(self):
        return '<Deck {}>'.format(self.name)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(240))
    answer = db.Column(db.String(240))
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'))

    def __repr__(self):
        return '<question {}>'.format(self.body)






