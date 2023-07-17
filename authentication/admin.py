import pymysql

from models import User,database

from config import Configuration


def createAdmin():
    connection = pymysql.connect(host='localhost',
                                 port=3306,
                                 user='root',
                                 password='root',
                                 database='authentication',
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        query = "SELECT * FROM users WHERE email=%s"
        cursor.execute(query, ('admin@admin.com',))
        result = cursor.fetchone()
        if (not result):
            sql = "INSERT INTO users (forename,surname,email, password,isCustomer, role) VALUES ('admin','admin','admin@admin.com', '1',False,'admin')"
            cursor.execute(sql)
        connection.commit()
    return


if __name__ == '__main__':
    createAdmin()