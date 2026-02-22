# Library that connects python to mySQL
import mysql.connector
# I'm not sure where this is being imported from...
# CharGPT: "Error → a class for catching connection or query errors in a try/except block."
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env into environment

# "Wrapper function" that is used to call another function
class Connection_Manager:
    def __init__(self):
        self.connected = False

    def _create_db_connection(self):
        """Internal method to establish a MySQL connection"""
        try:
            connection = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )
        except Error as err:
            print(err)
            return None
        else:
            self.connected = True
            self.connection = connection
            return connection

    def handle_SQL(self, query_func, commit=False, **kwargs):
        """
        Executes a SQL function that takes a cursor and optional keyword arguments.

        Parameters:
            query_func: the function that takes a cursor (and optional kwargs)
            commit: True if the SQL function performs an insert/update/delete
            **kwargs: any additional keyword arguments the SQL function needs
        """
        conn = self._create_db_connection()
        cursor = conn.cursor(dictionary=True)
        results = query_func(cursor, **kwargs)

        if commit:
            conn.commit()

        cursor.close()
        conn.close()
        return results