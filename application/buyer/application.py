import csv
import json
import os
import time
from datetime import datetime, date
import io

from flask import Flask, request, Response, jsonify
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from sqlalchemy import or_, and_, func
from redis import Redis
from collections import OrderedDict

from config import Configuration
from decorater import roleCheck, customerCheck
from models import database, ProductCategory, Product, Category, Order, Statistics

app = Flask(__name__)
app.config.from_object(Configuration)
jwt = JWTManager(app)


@app.route("/search", methods=["GET"])
@customerCheck(isCustomer=True)
@roleCheck(role="user")
@jwt_required(refresh=False)
def search():
    claims = get_jwt()
    name = request.args.get("name", "")
    category = request.args.get("category", "")

    categories = Category.query.join(ProductCategory).join(Product).with_entities(Category.name).filter(
        and_(Product.name.like("%{}%".format(name)), Category.name.like("%{}%".format(category)))
    ).group_by(Category.name).all()

    categories = [cat[0] for cat in categories]
    #print(categories)

    products = Product.query.join(ProductCategory).join(Category).with_entities(Product.id,Product.name,Product.price, Product.quantity).filter(
        and_(Product.name.like("%{}%".format(name)), Category.name.like("%{}%".format(category)))
    ).group_by(Product.id).all()
    #print(products)


    items = []
    for pr in products:
        cat = ProductCategory.query.join(Category).with_entities(Category.name).filter(
            ProductCategory.idproduct == pr[0]
        ).all()

        cat = [c[0] for c in cat]
        item = {
            "categories" : cat,
            "id" : pr[0],
            "name" : pr[1],
            "price" : pr[2],
            "quantity" : pr[3]
        }
        items.append(item)

    return jsonify(categories = categories, products = items), 200

@app.route('/order', methods=["POST"])
@customerCheck(isCustomer=True)
@roleCheck(role="user")
def order():
    claims=get_jwt()
    email = claims["email"]
    requests = request.json.get("requests", "")

    if(len(requests)<= 0):
        return jsonify(message="Field requests is missing."), 400

    index = 0
    cost = 0
    products = []
    for req in requests:
        if(not "id" in req):
            return jsonify(message="Product id is missing for request number {}.".format(index)), 400
        if(not "quantity" in req):
            return jsonify(message="Product quantity is missing for request number {}.".format(index)), 400

        id = req["id"]
        quantity = req["quantity"]

        try:
            id=int(id)
            if(id <= 0):
                return jsonify(message="Invalid product id for request number {}.".format(index)), 400
        except ValueError:
            return jsonify(message="Invalid product id for request number {}.".format(index)), 400

        try:
            quantity= int(quantity)
            if(quantity<=0):
                return jsonify(message="Invalid product quantity for request number {}.".format(index)), 400
        except ValueError:
            return jsonify(message="Invalid product quantity for request number {}.".format(index)), 400

        product = Product.query.filter(Product.id == id).first()
        products.append(product)
        if(not product):
            return jsonify(message="Invalid product for request number {}.".format(index)), 400
        cost += quantity*product.price
        index = index+1

    order = Order(price=cost, status="PENDING", timestamp=datetime.now(), user=email)
    database.session.add(order)
    database.session.commit()

    flag = True
    for i in range(len(requests)):
        amountStorage = products[i].quantity
        amountWanted = requests[i]["quantity"]
        if(amountStorage > amountWanted):
            amountStorage = amountWanted
        if(amountStorage < amountWanted):
            flag = False
        products[i].quantity -= amountStorage
        req = Statistics(price=products[i].price, requested=amountWanted, received=amountStorage, productId=products[i].id, orderId=order.id)
        database.session.add(req)

    if(flag):
        order.status = "COMPLETE"
    database.session.commit()
    return jsonify(id=order.id), 200

@app.route('/status',methods=["GET"])
@customerCheck(isCustomer=True)
@jwt_required(refresh=False)
def status():
    claims = get_jwt()
    email = claims["email"]

    items =[]

    ordersIds = Order.query.filter(Order.user == email).with_entities(Order.id, Order.price, Order.status, Order.timestamp).all()
    for ord in ordersIds:
        orders = Order.query.join(Statistics).join(Product).with_entities(Product.id,Product.name,Statistics.price,Statistics.received,Statistics.requested).filter(Order.id == ord[0]).all()
        prods =[]
        for o in orders:
            categories = Category.query.join(ProductCategory).with_entities(Category.name).filter(ProductCategory.idproduct == o[0]).group_by(Category.name).all()
            categories = [cats[0] for cats in categories]

            item = {
                "categories" : categories,
                "name" : o[1],
                "price" : o[2],
                "received" : o[3],
                "requested" : o[4]
            }
            prods.append(item)

        item = OrderedDict({
            "products" : prods,
            "price" : ord[1],
            "status" : ord[2],
            "timestamp" : ord[3]
        })
        items.append(item)

    return jsonify(orders=items), 200


@app.route('/')
def hello_world():
    return 'Dobrodosli na stranicu za kupce!'


if __name__ == '__main__':
    #os.environ['TZ'] = 'Europe/Belgrade'
    #time.tzset()
    database.init_app(app)
    app.run(debug=True, host='0.0.0.0', port=5002)