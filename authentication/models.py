from flask_sqlalchemy import SQLAlchemy;

database = SQLAlchemy();


class User(database.Model):
    __tablename__ = "users"

    id = database.Column(database.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    forename = database.Column(database.String(256), nullable=False)
    surname = database.Column(database.String(256), nullable=False)
    email = database.Column(database.String(256), nullable=False, unique=True)
    password = database.Column(database.String(256), nullable=False)
    isCustomer = database.Column(database.Boolean, nullable=False)
    role = database.Column(database.String(50),nullable=False)

    def __repr__(self):
        return "({}, {}, {})".format(self.email, self.forename, self.surname)