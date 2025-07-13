from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    melodies = db.relationship('Melody', backref='user', lazy=True)

class Melody(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blood_type = db.Column(db.String(10), nullable=False)
    eye_color = db.Column(db.String(20), nullable=False)
    origin = db.Column(db.String(100), nullable=False)
    mood = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
