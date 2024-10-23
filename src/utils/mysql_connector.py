import mysql.connector
from mysql.connector import Error
import traceback

class MySQLConnector:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            traceback.print_exc()

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")

    def execute_query(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            cursor.close()  # Asegúrate de cerrar el cursor
            return cursor
        except Error as e:
            print(f"Error executing query: {e}")
            traceback.print_exc()
            return None

    def fetch_all(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()  # Asegúrate de cerrar el cursor
            return result
        except Error as e:
            print(f"Error fetching all: {e}")
            traceback.print_exc()
            return []

    def fetch_one(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()  # Asegúrate de cerrar el cursor
            return result
        except Error as e:
            print(f"Error fetching one: {e}")
            traceback.print_exc()
            return None