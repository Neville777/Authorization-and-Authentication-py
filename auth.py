from flask import Blueprint, jsonify
from models import User, db, TokenBlockList
from flask_restful import reqparse, Resource, Api
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, JWTManager, get_jwt, jwt_required, verify_jwt_in_request, create_refresh_token
from functools import wraps
from datetime import datetime


# Create a JWTManager instance
jwt = JWTManager()

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["role"] == 5544:
                return fn(*args, **kwargs)
            else:
                return {"msg":"Admins only!"}, 403
            
        return decorator
    return wrapper

# Define a user lookup loader for JWT
@jwt.user_lookup_loader
def user_lookup_callback(__jwt__header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).first()

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload:dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlockList.id).filter_by(jti=jti).scalar()
    
    return token is not None

# Create a Blueprint for authentication
auth_bp = Blueprint('auth', __name__)

# Create an Api instance for the authentication Blueprint
api = Api(auth_bp)

# Define request parsers for registration and login
register_args = reqparse.RequestParser()
register_args.add_argument('email', required=True, help="Email is required")
register_args.add_argument('password', required=True, help="Password is required")

login_args = reqparse.RequestParser()
login_args.add_argument('email', required=True, help="Email is required")
login_args.add_argument('password', required=True, help="Password is required")

# Define resource classes for user registration and login
class UserRegister(Resource):
    def post(self):
        data = register_args.parse_args()
        # Generate password hash
        password_hash = generate_password_hash(data['password'])  
        # Create a new user instance
        user = User(email=data.get('email', None), password=password_hash)
        # Add user to the database session and commit changes
        db.session.add(user)
        db.session.commit()
        # Return user data as dictionary
        return user.to_dict()

class LoginUser(Resource):
    def post(self):
        data = login_args.parse_args()
        # Query user by email
        user = User.query.filter_by(email=data.get('email')).first()
        if user:
            # Check password hash
            if check_password_hash(user.password, data.get('password')):
                # Create access token for the user
                token = create_access_token(identity=user.id)
                return token

class LoginLogoutUser(Resource):
    def post(self):
        data = login_args.parse_args()
        user = User.query.filter_by(email=data.get('email')).first()
        print(user)
        if user:
            if check_password_hash(user.password, data.get('password')):
                access_token = create_access_token(
                    identity=user.id
                )
                refresh_token = create_refresh_token(identity = user.id)
                return {
                    "token":access_token,
                    "refresh":refresh_token
                }
        return {"msg" : "not logged in"}
    
    @jwt_required()
    def get(self):
        jwt_data = get_jwt()
        blocked_token = TokenBlockList(
            jti=jwt_data.get('jti'), created_at=datetime.utcnow())
        db.session.add(blocked_token)
        db.sesion.commit()
        return {"msg": "user logged out successfully"}
        
class UserManagement(Resource):
    
    @admin_required()
    def get(self):
        users = User.query.all()
        return [user.to_dict() for user in users]


# Add resources to the authentication API
api.add_resource(UserRegister, '/register')
api.add_resource(LoginLogoutUser, '/login')
api.add_resource(UserManagement, '/manage_users')