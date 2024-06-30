import pymysql


def init_db(host="127.0.0.1", user="root", password="123456", db="aifunbot"):
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        db=db,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )
    return connection


db_conn = init_db()
