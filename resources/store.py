from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json() # default is 200, so not necessary to put i tthere
        return {"message": "Store not found"}, 404 # at the end return a tuple with ({}, code)

    def post(self, name):
        if StoreModel.find_by_name(name):
            print("Error?------------------------------------------------------------")
            return {"message": f"Store '{name}' already exists"}, 400
            # return jsonify({"message", "Store already exists"}), 400
        store = StoreModel(name)
        try: 
            store.save_to_db()
        except:
            return {"message": "An error while creating the store"}, 500 # internal server error
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {"message": "Store deleted"}
        return {"message": "Error ocurred deleting the store"}


class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]} # item.json() for item in ItemModel.query.all()