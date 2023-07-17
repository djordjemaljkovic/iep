import csv
import json
import os
import time
from datetime import datetime, date
import io

from flask import Flask, request, Response, jsonify
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from sqlalchemy import or_, and_, func, desc, asc
from sqlalchemy.sql.functions import coalesce
from redis import Redis

from config import Configuration
from decorater import roleCheck
from models import database, ProductCategory, Product, Category, Order, Statistics

app = Flask(__name__)
app.config.from_object(Configuration)
jwt = JWTManager(app)

@app.route('/productStatistics', methods=["GET"])
@roleCheck(role="admin")
def productStatistics():
    claims=get_jwt()

    productInfo = Product.query.join(Statistics).with_entities(Product.name, func.sum(Statistics.requested), func.sum(Statistics.received)).group_by(Product.id, Product.name).all()

    info = []

    for i in productInfo:
        item = {
            "name" : i[0],
            "sold" : int(str(i[1])),
            "waiting" : int(str(i[1]-i[2]))
        }
        info.append(item)

    return jsonify(statistics=info),200


@app.route('/categoryStatistics', methods=["GET"])
@roleCheck(role="admin")
def categoryStatistics():
    claims = get_jwt()

    categoryInfo = Category.query.join(ProductCategory).join(Statistics, ProductCategory.idproduct==Statistics.productId).with_entities(Category.name).group_by(Category.id, Category.name).order_by(desc(func.sum(Statistics.requested)),asc(Category.name)).all()
    categoryInfo = [cat[0] for cat in categoryInfo]
    return jsonify(statistics=categoryInfo), 200

@app.route('/')
def helloWorld():
    return 'Dobrodosli na stranicu za admina!'


if(__name__ == "__main__"):
    database.init_app(app)
    app.run(debug=True,host="0.0.0.0",port=5003)

