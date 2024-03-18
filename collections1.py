from flask import Blueprint

collections_bp = Blueprint('collections,__name__')

class collections():
    
    def get():
        pass
    def post():
        pass
    
class CollectionsById():
    def get(self, id):
        pass
    def patch(self, id):
        pass
    def delete(self, id):
        pass