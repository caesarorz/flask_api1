# import sqlite3
from db import db

class ItemModel(db.Model):
    __tablename__ = 'items' 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel') # sql join

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {"name": self.name, "price": self.price}

    @classmethod
    def find_by_name(cls, name):
        """# saying "SELECT * FROM items WHERE name=name LIMIT 1" items= __tablenames__
        # it's returning an item model object
        return ItemModel.query.filter_by(name=name).first() 
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "SELECT * FROM items WHERE name=?"
        # result = cursor.execute(query, (name,))
        # row = result.fetchone()
        # connection.close()
        # if row:
        #     return cls(*row) # return cls(row[0], row[1])
        # return cls.query.filter_by(name=name).first()""" 
        return cls.query.filter_by(name=name).first() 

    def delete_from_db(self):
        db.session.delete(self) # the session is a collection of objects that we are going to write
        db.session.commit() # to the database
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "UPDATE items SET price=? WHERE name=?"
        # cursor.execute(query, (self.price, self.name))
        # connection.commit()
        # connection.close()

    def save_to_db(self): 
        """save it or update it to the db """
        # sqlalchemy can translate directly from object to row
        db.session.add(self)
        db.session.commit()
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "INSERT INTO items VALUES (?, ?)"
        # cursor.execute(query, (self.name, self.price))
        # connection.commit()
        # connection.close()        