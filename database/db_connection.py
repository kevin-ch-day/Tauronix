import mysql.connector
from . import db_config

def create_connection():
    try:
        connection = mysql.connector.connect(
            host=db_config.DB_HOST,
            user=db_config.DB_USER,
            password=db_config.DB_PASSWORD,
            database=db_config.DB_DATABASE
        )
        return connection
    
    except mysql.connector.Error as e:
        print("Error connecting to MySQL database:", e)
        return None

def close_connection(connection):
    try:
        if connection.is_connected():
            connection.close()
    except mysql.connector.Error as e:
        print("Error closing MySQL connection:", e)

def execute_query(connection, query, data=None):
    try:
        if connection.is_connected():
            cursor = connection.cursor()
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)

            result = cursor.fetchall()
            cursor.close()
            return result
    
    except mysql.connector.Error as e:
        print("Error executing SQL query:", e)
        return None

def delete_data(connection, query, data=None):
    try:
        if connection.is_connected():
            cursor = connection.cursor()
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            
            connection.commit()
            cursor.close()
            return True
        
        else:
            print("Connection is not established.")
            return False
    
    except mysql.connector.Error as e:
        print("Error deleting data:", e)
        return False

