from flask import Blueprint
from models import Collection, db
from flask_restful import reqparse, Resource, Api
from flask_jwt_extended import jwt_required


collections_bp = Blueprint('collections_dp', __name__)

api = Api(collections_bp)

class Collections(Resource):
    
    @jwt_required()
    def get(self):
        collections = Collection.query.all()
        return collections
    
    @jwt_required()
    def post(self):
        pass
    
class CollectionsById(Resource):
    
    @jwt_required()
    def get(self, id):
        collection = Collection.query.filter_by(id=id).first()
        return collection
    
    @jwt_required()
    def patch(self, id):
        collection = Collection.query.filter_by(id=id).first()
        
    @jwt_required()
    def delete(self, id):
        pass
    
api.add_resource(Collections, '/collections')
api.add_resource(CollectionsById, '/collections/<int:id>')