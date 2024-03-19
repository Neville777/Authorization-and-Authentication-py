from flask import Blueprint
from models import Collection, db
from flask_restful import reqparse, Resource, Api


collections_bp = Blueprint('collections_dp', __name__)

api = Api(collections_bp)

class Collections(Resource):
    
    def get(self):
        collections = Collection.query.all()
        return collections
    
    def post(self):
        pass
    
class CollectionsById(Resource):
    def get(self, id):
        collection = Collection.query.filter_by(id=id).first()
        return collection
    
    
    def patch(self, id):
        collection = Collection.query.filter_by(id=id).first()
        
    def delete(self, id):
        pass
    
api.add_resource(Collections, '/collections')
api.add_resource(CollectionsById, '/collections/<int:id>')