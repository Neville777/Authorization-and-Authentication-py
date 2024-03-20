from flask import Blueprint
from models import User, db
from flask_restful import reqparse, Resource, Api
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, JWTManager

# Create a JWTManager instance
jwt = JWTManager()

# Define a user lookup loader for JWT
@jwt.user_lookup_loader
def user_lookup_callback(__jwt__header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).first()

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

# Add resources to the authentication API
api.add_resource(UserRegister, '/register')
api.add_resource(LoginUser, '/login')
