# import sqlite3 no longer needed
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from resources.user import UserRegister
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
            type=float,
            required=True,
            help='This field cannot be left blank'
        )

    parser.add_argument('store_id',
            type=int,
            required=True,
            help='Every item needs a store id'
        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json() # return item # because we are returning an item object now, not an dict
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name): # I can user Item.find_by_name(name): because is a class method 
            return {"message": "The item already exists"}, 400
        data = Item.parser.parse_args()
        # item = {"name": name, "price": data["price"]} should not be a dict but an item object
        item = ItemModel(name, **data) # data['price'], data['store_id']) = **data
        try:
            item.save_to_db()
        except:
            return {"message": "Item could not be inserted"}, 500
        return item.json(), 201

    def put(self, name):
        data = Item.parser.parse_args()
        # item = next(filter(lambda x: x['name'] == name, items), None)
        item = ItemModel.find_by_name(name)
        # updated_item = ItemModel(name, data["price"])
        if item is None:
            try: 
                item = ItemModel(name, **data) # data['price'], data['store_id']             
                # updated_item.insert()# ItemModel.insert(updated_item)
            except:
                return {"message": "Error inserting the item"}, 500
        else:
            item.price = data['price'] 
            # item.store_id = data['store_id']   
        item.save_to_db()
        # return updated_item.json()
        return item.json()

    def delete(self, name):
        item = Item.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message": "Item deleted"}


class ItemList(Resource):
    def get(self):
        # return {'items': [item.json() for item in ItemModel.query.all()]}
        # using lambda function
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}

