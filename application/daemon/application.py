from flask import Flask
from flask_jwt_extended import JWTManager
import datetime
import os
import threading
import time
from datetime import datetime

from redis import Redis
from sqlalchemy import and_, orm, asc, func

from models import Product, Order, Category, Statistics, ProductCategory, database
from config import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)
jwt = JWTManager(app)


def deamon():
    while (1):
        try:
            with Redis(Configuration.REDIS_HOST) as redis:
                while (1):
                    bytes = redis.blpop(Configuration.REDIS_PRODUCTS_LIST)[1].decode().split(",")

                    kategorije = bytes[0].split("|")
                    ime = bytes[1]
                    kolicina = int(bytes[2])
                    cena = float(bytes[3])
                    print(str(bytes))

                    with app.app_context():
                        productNameDuplicated = database.session.query(Product).filter(Product.name == ime).first()
                        print(productNameDuplicated)
                        if(productNameDuplicated):
                            productExists = database.session.query(ProductCategory).join(Category).with_entities(Category.name).filter(ProductCategory.idproduct == productNameDuplicated.id).all()
                            productExists = [p[0] for p in productExists]
                            print(productExists)
                            if(set(kategorije) == set(productExists)):
                                productNameDuplicated.price = (productNameDuplicated.quantity*productNameDuplicated.price + cena*kolicina) / (productNameDuplicated.quantity + kolicina)
                                productNameDuplicated.quantity += kolicina
                                database.session.commit()
                                print(productNameDuplicated)

                                orderWaiting = database.session.query(Order).join(Statistics).with_entities(Order.id, Statistics.id).filter(
                                    Order.status == "PENDING",
                                    Statistics.productId == productNameDuplicated.id,
                                    Statistics.received < Statistics.requested
                                ).group_by(Order.id, Statistics.id).order_by(asc(Order.id)).all()

                                for o in orderWaiting:
                                    order = database.session.query(Order).filter(Order.id == o[0]).first()
                                    req = database.session.query(Statistics).filter(Statistics.id == o[1]).first()
                                    count = database.session.query(Statistics).with_entities(func.cont("*")).filter(
                                        Statistics.orderId == order.id,
                                        Statistics.received < Statistics.requested
                                    ).all()
                                    print("usao3")

                                    amountMissing = req.requested - req.received
                                    if (amountMissing < productNameDuplicated.quantity):
                                        productNameDuplicated.quantity -= amountMissing
                                        req.received += amountMissing
                                        print("usao4")
                                        if(count[0][0] == 1):
                                            order.status = "COMPLETE"
                                            print("usao5")
                                    else:
                                        req.received += productNameDuplicated.quantity
                                        productNameDuplicated.quantity = 0
                                        print("usao6")
                                    database.session.commit()
                                    if (productNameDuplicated.quantity == 0):
                                        print("usao7")
                                        break;
                            else:
                                print("usao8")
                                continue;
                        else:
                            newProduct = Product(name = ime, price=cena, quantity = kolicina)
                            database.session.add(newProduct)
                            database.session.commit()
                            print(newProduct)
                            for c in kategorije:
                                newCategory = database.session.query(Category).filter(Category.name == c).first()
                                if (not newCategory):
                                    newCategory = Category(name = c)
                                    database.session.add(newCategory)
                                    database.session.commit()
                                    print(newCategory)
                                newRelationship = ProductCategory(idproduct= newProduct.id, idcategory=newCategory.id)
                                database.session.add(newRelationship)
                                database.session.commit()
                                print(newRelationship)

        except Exception as e:
            print(e)

if __name__ == '__main__':
    database.init_app(app)
    deamon()