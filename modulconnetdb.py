import mysql.connector as sql

db_conf = {
        'host': 'localhost',
        'user': 'root',
        'password': 'ichyyyyy'
    }

def connect(db_config):

    print(type(db_config))
    # Biến lưu trữ kết nối
    conn = None

    try:
        conn = sql.MySQLConnection(**db_config)

        if conn.is_connected():
            return conn

    except sql.Error as error:
        print(error)

    return conn


def arr_message():
    arr_messages = []
    db_config = db_conf
    db_config['database'] = 'chat'
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM chat.chatroom;")

        row = cursor.fetchone()

        while row is not None:
            arr_messages.append(row)
            row = cursor.fetchone()

    except sql.Error as e:
        print(e)

    finally:
        # Đóng kết nối
        cursor.close()
        conn.close()

    return arr_messages


def delete_database():
    query = "DELETE FROM chat.chatroom;"
    conn = connect(db_conf)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()


def create_database():
    query1 = "CREATE DATABASE IF NOT EXISTS `chat`;"
    query2 = "CREATE TABLE IF NOT EXISTS `chat`.`chatroom` (`user` VARCHAR(45) NULL DEFAULT NULL,`text` TEXT NULL DEFAULT NULL,`datetimechat` DATETIME NULL DEFAULT NULL)ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;"
    conn = connect(db_conf)

    cursor = conn.cursor()
    cursor.execute(query1)
    cursor.execute(query2)



def insert_message(user, text, datetime):
    query = "INSERT INTO chat.chatroom( user, text, datetimechat) " \
            "VALUES(%s,%s,%s)"
    # INSERT INTO `chat`.`chatroom`(`user`, `text`, `datetimechat`) VALUES('dnt', '456', '2021-05-15 13:00:00');

    args = (user, text, datetime)
    db_config = db_conf
    db_config['database'] = 'chat'
    try:
        conn = connect(db_config)

        cursor = conn.cursor()
        cursor.execute(query, args)

        if cursor.lastrowid:
            print('ID insert là:', cursor.lastrowid)
        else:
            print(cursor)
            # print('Insert thất bại')

        conn.commit()
    except sql.Error as error:
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
#conn = connect()
# print(conn)
# delete_database()
create_database()
# load_old_message()

# insert_book('dnt', 'huhu', '2021-10-15 22:22:22')
