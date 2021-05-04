from mysql.connector import MySQLConnection, Error
import datetime
def connect():
    db_config = {
        'host': 'localhost',
        'database': 'chat',
        'user': 'root',
        'password': 'ichyyyyy'
    }

    # Biến lưu trữ kết nối
    conn = None

    try:
        conn = MySQLConnection(**db_config)

        if conn.is_connected():
            return conn

    except Error as error:
        print(error)

    return conn


def show_message():
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM chat.chatroom;")

        row = cursor.fetchone()

        while row is not None:
            print(row)
            row = cursor.fetchone()

    except Error as e:
        print(e)

    finally:
        # Đóng kết nối
        cursor.close()
        conn.close()


def insert_message(user, text, datetime):
    query = "INSERT INTO chat.chatroom(user, text, datetimechat) " \
            "VALUES(%s,%s,%s)"
    # INSERT INTO `chat`.`chatroom`(`user`, `text`, `datetimechat`) VALUES('dnt', '456', '2021-05-15 13:00:00');

    args = (user, text, datetime)

    try:
        conn = connect()

        cursor = conn.cursor()
        cursor.execute(query, args)

        if cursor.lastrowid:
            print('ID insert là:', cursor.lastrowid)
        else:
            print('Insert thất bại')

        conn.commit()
    except Error as error:
        print(error)

    finally:
        # Đóng kết nối
        cursor.close()
        conn.close()

# Test thử
# conn = connect()
# print(conn)
# show_books()
# insert_book('dnt', 'huhu', '2021-10-15 22:22:22')