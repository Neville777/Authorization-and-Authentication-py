from flask import Blueprint, jsonify
from models import User, db, TokenBlockList
from flask_restful import reqparse, Resource, Api
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token,get_jwt_identity, JWTManager, get_jwt, jwt_required, verify_jwt_in_request, create_refresh_token
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

@jwt.additional_claims_loader
def add_claims_to_access_token(identity):
    user = User.query.filter_by(id=identity).first()
    return {
        "role":2201,
        "name":user.email
    }

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
class LoginLogoutUser(Resource):
    def post(self):
        # Parse incoming request arguments
        data = login_args.parse_args()
        # Query user by email
        user = User.query.filter_by(email=data.get('email')).first()
        print(user)
        # Check if user exists and password is correct
        if user:
            if check_password_hash(user.password, data.get('password')):
                # Generate access token for the user
                access_token = create_access_token(identity=user.id)
                # Generate refresh token for the user
                refresh_token = create_refresh_token(identity=user.id)
                # Return access and refresh tokens in response
                return {
                    "token": access_token,
                    "refresh": refresh_token
                }
        # If user not found or password is incorrect, return appropriate message
        return {"msg": "not logged in"}
    
    @jwt_required(refresh=True)
    def get(self):
        identity = get_jwt_identity()
        new_token = create_access_token(identity=identity)
        return {"token":new_token}
    
class Logout(Resource):
    
    @jwt_required()
    def get(self):
        # Retrieve JWT data from the request
        jwt_data = get_jwt()
        # Create a TokenBlocklist entry for the JWT token to invalidate it
        blocked_token = TokenBlockList(
            jti=jwt_data.get('jti'), created_at=datetime.utcnow())
        # Add the TokenBlocklist entry to the database session
        db.session.add(blocked_token)
        # Commit changes to the database
        db.sesion.commit()
        # Return a success message indicating user logout
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