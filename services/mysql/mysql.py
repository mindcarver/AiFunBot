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


## /start 记录用户数据到数据库
def insert_user(user_id, invite_code, user_type):
    with db_conn.cursor() as cursor:
        sql = "INSERT INTO `users` (`user_id`, `invite_code`, `user_type`) VALUES (%s, %s, %s)"
        cursor.execute(sql, (user_id, invite_code, user_type))
        db_conn.commit()
