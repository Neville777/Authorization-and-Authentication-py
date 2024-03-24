import os
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db
from datetime import timedelta
from collections1 import collections_bp  
from auth import auth_bp, jwt  

# Create Flask application instance
app = Flask(__name__)

# Configure application settings
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///db.db'  # SQLite database URI
app.config['SECRET_KEY'] = 'jwt36v-12hrv2;sfqwf87a'  # Secret key for JWT
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable Flask-SQLAlchemy modification tracking
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=2)  # JWT access token expiration time
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)  # JWT refresh token expiration time']
app.json.compact = False  # Compact JSON response format

# Register blueprints for different parts of the application
app.register_blueprint(collections_bp)  
app.register_blueprint(auth_bp)  

# Initialize Flask-Migrate for database migrations
db.init_app(app)
migrate = Migrate(app, db)

# Initialize JWT manager
jwt.init_app(app)

# run the Flask application

if __name__ == "__main__":
    app.run()
