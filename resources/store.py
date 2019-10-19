from flask_restful import Resource
from flask_jwt import jwt_required
from models.store import StoreModel

class StoreRegister(Resource):
    @jwt_required()
    def post (self, name):
        if StoreModel.find_by_name(name):
            return {'message': 'A store with this name already exists!'}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            {'message': 'An unexpected error has occurred!'}, 500
        return store.json(), 201

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return {'message': 'A store with this name does not exist!'}, 404

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store is None:
            return {'message': 'This store does not exist'}, 404
        store.delete_from_db()
        return {'message': 'The item has been deleted'}

class StoreList(Resource):
    @jwt_required()
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
