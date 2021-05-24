from mysql.connector import MySQLConnection, Error
from dbconnector import read_db_config

def insert_notification(message,time, userID, camID):
    query = "INSERT INTO notifications(message,time, userID, camID) " \
            "VALUES(%s,%s,%s,%s)"
    args = (message,time, userID, camID)

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.execute(query, args)

        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')

        conn.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()

def main():
   insert_notification('Today\'s Notification','2021-05-12 11:19:29', 1, 2)

if __name__ == '__main__':
    main()