import mysql.connector
from mysql.connector import Error

def queryDB(connection, query):
    cursor = connection.cursor(buffered=True)
    try:
        cursor.execute(query)
        return cursor
    except Error as e:
        print(f"The error '{e}' occurred")

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection