from flask import Flask, request, Response, jsonify
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt

from decorater import roleCheck
from config import Configuration
from models import database, User
from sqlalchemy import or_, and_
from registrationCheck import RegistrationCheck
from markupsafe import escape

app = Flask(__name__)
app.config.from_object(Configuration)
jwt = JWTManager(app)


@app.route('/')
def hello_world():
    return 'Dobrodosli u sistem za upravljanje prodavnicom!'


@app.route('/korisnici', methods=["GET"])
def proba():
    svi = User.query.all()
    return str(svi)

#Registracija korisnika
@app.route('/register', methods=["POST"])
def register():
    forename = request.json.get("forename", "");
    surname = request.json.get("surname", "");
    email = request.json.get("email", "");
    password = request.json.get("password", "");
    isCustomer = request.json.get("isCustomer", "");

    registrationCheck = RegistrationCheck( forename, surname,email, password, isCustomer)
    message = registrationCheck.EmptyCheck()
    if (message != ""):
        return jsonify(message=message), 400;
    message = registrationCheck.EmailCheck()
    if (message != ""):
        return jsonify(message=message), 400;
    message = registrationCheck.PasswordCheck()
    if (message != ""):
        return jsonify(message=message), 400;

    user = User.query.filter(User.email == email).first()
    if (user):
        return jsonify(message="Email already exists."), 400;


    user = User(forename=forename, surname=surname, email=email, password=password, isCustomer = isCustomer, role="user")
    database.session.add(user)
    database.session.commit()

    return Response(status=200);

#Prijava korisnika
@app.route('/login', methods=["POST"])
def login():
    email = request.json.get("email", "");
    password = request.json.get("password", "");

    registrationCheck = RegistrationCheck("forename", "surname", email, password, "isCustomer")
    message = registrationCheck.EmptyCheck()
    if (message != ""):
        return jsonify(message=message), 400;
    message = registrationCheck.EmailCheck()
    if (message != ""):
        return jsonify(message=message), 400;

    user = User.query.filter(and_(User.email == email, User.password == password)).first();
    if (not user):
        return jsonify(message="Invalid credentials."), 400;

    additionalClaims = {
        "forename": user.forename,
        "surname": user.surname,
        "email": user.email,
        "password": user.password,
        "isCustomer": user.isCustomer,
        "role": user.role
    }

    accessToken = create_access_token(identity=user.email, additional_claims=additionalClaims);
    refreshToken = create_refresh_token(identity=user.email, additional_claims=additionalClaims);

    return jsonify(accessToken=accessToken, refreshToken=refreshToken);


@app.route("/check",methods=["POST"])
@jwt_required()
def check():
    return "Token is valid.";

@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity();
    refreshClaims = get_jwt();

    additionalClaims = {
        "forename": refreshClaims["forename"],
        "surname": refreshClaims["surname"],
        "email": refreshClaims["email"],
        "password": refreshClaims["password"],
        "isCustomer": refreshClaims["isCustomer"],
        "role": refreshClaims["role"]
    };

    return jsonify(accessToken=create_access_token(identity=identity, additional_claims=additionalClaims)), 200


@app.route("/delete", methods=["POST"])
@jwt_required(refresh=False)
@roleCheck(role="admin")
def delete():
    email = request.json.get("email", "");
    registrationCheck = RegistrationCheck( "forename", "surname",email, "password", "isCustomer")
    message = registrationCheck.EmptyCheck()
    if (message != ""):
        return jsonify(message=message), 400;
    message = registrationCheck.EmailCheck()
    if (message != ""):
        return jsonify(message=message), 400;

    user = User.query.filter(User.email == email).first()
    if (not user):
        return jsonify(message="Unknown user."), 400;
    database.session.delete(user)
    database.session.commit()

    return Response(status=200);


if __name__ == '__main__':
    database.init_app(app)
    app.run(debug=True, host="0.0.0.0", port=5000)