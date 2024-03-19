import os
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db
from collections1 import collections_bp
from auth import auth_bp

app = Flask(__name__)

# Corrected the config key to 'SQLALCHEMY_DATABASE_URI'
app.config['SQLALCHEMY_DATABASE_URI'] =  os.environ.get('DATABASE_URI') or'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
app.register_blueprint(collections_bp)
app.register_blueprint(auth_bp)

# Initialize Migrate
db.init_app(app)

migrate = Migrate(app, db)

