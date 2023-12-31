from datetime import timedelta;
import os;

path = os.environ["DATABASE_URL"]
#path = "localhost:3307"


class Configuration():
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:root@{path}/application"
    JWT_SECRET_KEY = "JWTSecretDevKey"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta ( minutes = 60 );
    JWT_REFRESH_TOKEN_EXPIRES = timedelta ( days = 30 );