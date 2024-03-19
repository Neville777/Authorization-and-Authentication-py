from flask import Blueprint
from models import User, db
from flask_restful import reqparse, Resource, Api

auth_bp = Blueprint('auth', __name__)
api = Api(auth_bp)

register_args = reqparse.RequestParser()

register_args.add_argument('email',required=True, help="Name is required")
register_args.add_argument('password',required=True, help="Password is required")

class UserRegister(Resource):
    
    def post(self):
        data = register_args.parse_args()
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return {'message': 'User created successfully', 'user_id': user.id}, 201
    
api.add_resource(UserRegister ,'/register')