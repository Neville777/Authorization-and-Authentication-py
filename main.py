import os
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db
from datetime import timedelta
from collections1 import collections_bp
from auth import auth_bp, jwt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///db.db'
app.config['SECRET_KEY']='jwt36v-12hrv2;sfqwf87a'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.json.compact = False
app.register_blueprint(collections_bp)
app.register_blueprint(auth_bp)

# Initialize Migrate
db.init_app(app)
jwt.init_app(app)

migrate = Migrate(app, db)

