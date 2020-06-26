# import sqlite3
from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores' 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic') # many to one rela: onw store, many items

    def __init__(self, name):
        self.name = name

    def json(self): # using lazy='dynamic', self.stores is not a list of stores, is a query builder
        return {"name": self.name, "items": [item.json() for item in self.items.all()]} # that have the ability to look into the items table

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() 

    def delete_from_db(self):
        db.session.delete(self) # the session is a collection of objects that we are going to write
        db.session.commit() 


    def save_to_db(self): 
        """save it or update it to the db """
        # sqlalchemy can translate directly from object to row
        db.session.add(self)
        db.session.commit()
      