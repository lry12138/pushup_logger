from . import db
from flask_login import UserMixin
from datetime import date

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    workouts = db.relationship('Workout', backref='author', lazy='dynamic')

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pushups = db.Column(db.Integer, nullable = False)
    date = db.Column(db.DateTime, nullable = False, default = date.today())
    comment = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable = False)
