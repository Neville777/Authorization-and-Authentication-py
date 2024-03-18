import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, User, Collection, Profile
app = Flask(__name__)

# Corrected the config key to 'SQLALCHEMY_DATABASE_URI'
app.config['SQLALCHEMY_DATABASE_URI'] =  os.environ.get('DATABASE_URI') or'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Initialize Migrate
migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# Import your models here
from models import User  # Assuming you have a User model in models.py

# Define your routes and other configurations here
