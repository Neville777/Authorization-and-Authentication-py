from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    
    # Relationships
    profile = db.relationship('Profile', back_populates='user', uselist=False)
    collections = db.relationship('Collection', back_populates='user')

class Profile(db.Model, SerializerMixin):
    __tablename__ = 'profile'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    photo_url = db.Column(db.String)
    location = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    user = db.relationship('User', back_populates='profile', uselist=False)

class Collection(db.Model, SerializerMixin):
    serialize_only = ('name','photo_url','user_id')
    __tablename__ = 'collections'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    photo_url = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  
    
    # Relationships
    user = db.relationship('User', back_populates='collections')
