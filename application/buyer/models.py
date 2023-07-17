from sqlalchemy import orm, Column, Integer,Float, ForeignKey, String, Boolean, create_engine
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

from config import Configuration

#base = declarative_base()
#engine = create_engine(Configuration.SQLALCHEMY_DATABASE_URI)
#base.metadata.bind = engine

database = SQLAlchemy()

class ProductCategory(database.Model):
    __tablename__ = "productcategory"

    id = database.Column(database.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    idproduct = database.Column(database.Integer, database.ForeignKey("product.id"), nullable=False)
    idcategory = database.Column(database.Integer, database.ForeignKey("category.id"), nullable=False)

class Statistics(database.Model):
    __tablename__ = "statistics"

    id = database.Column(database.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    price = database.Column(database.Float, nullable=False)
    received = database.Column(database.Integer, nullable=False)
    requested = database.Column(database.Integer, nullable=False)

    #za koji proizvod i porudzbinu je vezana ova statistika
    productId = database.Column(database.Integer, database.ForeignKey("product.id"), nullable = False)
    orderId = database.Column(database.Integer, database.ForeignKey("order.id"), nullable=False)

    def __repr__(self):
        return "({}, {}, {}, {})".format(self.id, self.price, self.requested, self.received)


class Product(database.Model):
    __tablename__ = "product"

    id = database.Column(database.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    name = database.Column(database.String(256),nullable = False)
    price = database.Column(database.Float, nullable=False)
    quantity = database.Column (database.Integer, nullable = False)

    categories = database.relationship("Category", secondary=ProductCategory.__table__, back_populates="products")
    orders = database.relationship("Order", secondary=Statistics.__table__, back_populates="products")

    def __repr__(self):
        return "({}, {}, {})".format(self.name, self.price, self.quantity)

    def serializeFull(self):
        return {
            'id' : self.id,
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity
        }

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Category(database.Model):
    __tablename__ = "category"

    id = database.Column(database.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    name = database.Column(database.String(256), nullable = False)

    products = database.relationship("Product", secondary=ProductCategory.__table__, back_populates="categories")

    def serialize(self):
        return{
            'name' : self.name
        }


class Order(database.Model):
    __tablename__ = "order"

    id = database.Column(database.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    price = database.Column(database.Float, nullable =False)
    status = database.Column(database.String(256), nullable=False)
    timestamp = database.Column(database.DATETIME, nullable=False)
    user = database.Column(database.String(256), nullable=False)

    products = database.relationship("Product", secondary=Statistics.__table__, back_populates="orders")

    def serialize(self):
        return {
            'id': self.id,
            'price': self.price,
            'status': self.status,
            'timestamp': self.timestamp.strftime('%Y-%m-%d'),
            'products': [p.serialize() for p in self.products]
        }


