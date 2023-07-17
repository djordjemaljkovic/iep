from datetime import timedelta
import os

#path = os.environ["REDIS_URL"]
#path = "localhost"

class Configuration():
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3307/application"
    JWT_SECRET_KEY = "JWTSecretDevKey"
    REDIS_HOST = "redis"
    REDIS_PRODUCTS_LIST = "products"
    REDIS_SUBSCRIBE_CHANNEL = "hasItems"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta ( minutes = 60 );
    JWT_REFRESH_TOKEN_EXPIRES = timedelta ( days = 30 );