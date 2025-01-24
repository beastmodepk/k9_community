from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_active = db.Column(db.Boolean, default=False)  # Admin approval flag
    is_admin = db.Column(db.Boolean, default=False)   # For admin users
    dogs = db.relationship('Dog', back_populates='owner')

class Dog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    breed = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    temperament_with_kids = db.Column(db.String(120), nullable=False)
    temperament_with_dogs = db.Column(db.String(120), nullable=False)
    temperament_with_pets = db.Column(db.String(120), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    owner = db.relationship('User', back_populates='dogs')
