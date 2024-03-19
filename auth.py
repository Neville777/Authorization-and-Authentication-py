from flask import Blueprint
from models import User, db
from flask_restful import reqparse, Resource, Api
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, JWTManager

jwt = JWTManager()

auth_bp = Blueprint('auth', __name__)
api = Api(auth_bp)

register_args = reqparse.RequestParser()

register_args.add_argument('email', required=True, help="Email is required")
register_args.add_argument('password', required=True, help="Password is required")

login_args = reqparse.RequestParser()

login_args.add_argument('email', required=True, help="Email is required")
login_args.add_argument('password', required=True, help="Password is required")


class UserRegister(Resource):
    def post(self):
        data = register_args.parse_args()
        password_hash = generate_password_hash(data['password'])  
        user = User(email=data.get('email', None), password=password_hash)
        db.session.add(user)
        db.session.commit()
        return user.to_dict()


class LoginUser(Resource):
    def post(self):
        data = login_args.parse_args()
        user = User.query.filter_by(email=data.get('email')).first()
        if user:
            if check_password_hash(user.password, data.get('password')):
                token = create_access_token(identity=user.id)
                return token

api.add_resource(UserRegister, '/register')
api.add_resource(LoginUser, '/login')
