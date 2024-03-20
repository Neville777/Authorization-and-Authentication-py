from flask import Blueprint
from models import Collection, db
from flask_restful import reqparse, Resource, Api
from flask_jwt_extended import jwt_required, current_user, get_jwt_identity


collections_bp = Blueprint('collections_dp', __name__)

api = Api(collections_bp)

collection_args = reqparse.RequestParser()

collection_args.add_argument('name', required=True, help="Name is required")
collection_args.add_argument('photo_url', required=True, help="Photo_url is required")


class Collections(Resource):
    
    @jwt_required()
    def get(self):
        collections = Collection.query.filter_by(user_id=get_jwt_identity())
        return [collection.to_dict() for collection in collections]
    
    @jwt_required()
    def post(self):
        data = collection_args.parse_args()
        collection = Collection(name=data.get('name'),photo_url=data.get('photo_url'),user_id=get_jwt_identity())
        db.session.add(collection)
        db.session.commit()
        return collection.to_dict()
    
class CollectionsById(Resource):
    
    @jwt_required()
    def get(self, id):
        collection = Collection.query.filter_by(id=id).first()
        return collection.to_dict()
    
    @jwt_required()
    def patch(self, id):
        collection = Collection.query.filter_by(id=id).first()
        
    @jwt_required()
    def delete(self, id):
        pass
    
api.add_resource(Collections, '/collections')
api.add_resource(CollectionsById, '/collections/<int:id>')