from flask import Blueprint
from models import Collection, db
from flask_restful import reqparse, Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity

# Create a Blueprint for collections
collections_bp = Blueprint('collections_dp', __name__)

# Create an Api instance for the collections Blueprint
api = Api(collections_bp)

# Define request parser for collections
collection_args = reqparse.RequestParser()
collection_args.add_argument('name', required=True, help="Name is required")
collection_args.add_argument('photo_url', required=True, help="Photo_url is required")

# Define resource classes for handling collections
class Collections(Resource):
    
    @jwt_required()
    def get(self):
        # Retrieve collections associated with the authenticated user
        collections = Collection.query.filter_by(user_id=get_jwt_identity())
        return [collection.to_dict() for collection in collections]
    
    @jwt_required()
    def post(self):
        data = collection_args.parse_args()
        # Create a new collection
        collection = Collection(name=data.get('name'), photo_url=data.get('photo_url'), user_id=get_jwt_identity())
        # Add collection to the database session and commit changes
        db.session.add(collection)
        db.session.commit()
        return collection.to_dict()

# Define resource class for handling individual collection by ID
class CollectionsById(Resource):
    
    @jwt_required()
    def get(self, id):
        # Retrieve a specific collection by its ID
        collection = Collection.query.filter_by(id=id).first()
        return collection.to_dict()
    
    @jwt_required()
    def patch(self, id):
        # Logic for updating a specific collection
        pass
        
    @jwt_required()
    def delete(self, id):
        # Logic for deleting a specific collection
        pass

# Add resources to the collections API
api.add_resource(Collections, '/collections')
api.add_resource(CollectionsById, '/collections/<int:id>')
