import csv
from datetime import datetime
import io

from flask import Flask, request, Response, jsonify
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from redis import Redis

from decorater import customerCheck,roleCheck
from config import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)
jwt = JWTManager(app)

@app.route("/update", methods=["POST"])
@jwt_required(refresh=False)
@customerCheck(isCustomer= False)
@roleCheck(role="user")
def update():
    claims = get_jwt();
    try:
        content = request.files["file"].stream.read().decode("utf-8")
    except Exception:
        return jsonify(message="Field file is missing."), 400
    stream = io.StringIO(content)
    reader = csv.reader(stream)

    items = []
    index = 0
    for row in reader:
        if (len(row) != 4):
            return jsonify(message="Incorrect number of values on line {}.".format(index)), 400
        if (not row[2].isdecimal() or int(row[2]) <= 0):
            return jsonify(message="Incorrect quantity on line {}.".format(index)), 400
        try:
            float(row[3])
            if (float(row[3]) < 0):
                return jsonify(message="Incorrect price on line {}.".format(index)), 400
        except ValueError:
            return jsonify(message="Incorrect price on line {}.".format(index)), 400
        index += 1
        itemAdd = ",".join(row)
        items.append(itemAdd)


    for item in items:
        with Redis(host=Configuration.REDIS_HOST) as redis:
            redis.rpush(Configuration.REDIS_PRODUCTS_LIST, item)

    return Response("Uspesno poslato na redis!", status=200)


@app.route('/')
def hello():
    return "Dobrodosli u magacin", 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)