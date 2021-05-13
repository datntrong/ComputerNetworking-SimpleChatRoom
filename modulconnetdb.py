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


def arr_message():
    arr_messages = []
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM chat.chatroom;")

        row = cursor.fetchone()

        while row is not None:
            arr_messages.append(row)
            row = cursor.fetchone()

    except Error as e:
        print(e)

    finally:
        # Đóng kết nối
        cursor.close()
        conn.close()

    return arr_messages


def insert_message(user, text, datetime):
    query = "INSERT INTO chat.chatroom( user, text, datetimechat) " \
            "VALUES(%s,%s,%s)"
    # INSERT INTO `chat`.`chatroom`(`user`, `text`, `datetimechat`) VALUES('dnt', '456', '2021-05-15 13:00:00');

    args = ( user, text, datetime)

    try:
        conn = connect()

        cursor = conn.cursor()
        cursor.execute(query, args)

        if cursor.lastrowid:
            print('ID insert là:', cursor.lastrowid)
        else:
            print(cursor)
            # print('Insert thất bại')

        conn.commit()
    except Error as error:
        print(error)

    finally:
        # Đóng kết nối
        cursor.close()
        conn.close()

def load_old_message():
    arr_messages = arr_message()
    print(arr_messages)
    print(type(arr_messages))
    for i in arr_messages:
        message = i
        print(message[0])
        print(message[1])
        print(message[2])

# Test thử
conn = connect()
print(conn)
load_old_message()

# insert_book('dnt', 'huhu', '2021-10-15 22:22:22')