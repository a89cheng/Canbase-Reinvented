# Library that connects python to mySQL
import mysql.connector
# I'm not sure where this is being imported from...
# CharGPT: "Error → a class for catching connection or query errors in a try/except block."
from mysql.connector import Error

# "Wrapper function" that is used to call another function
def create_db_connection(host_name, user_name, user_password, db_name):
    """Establishes a connection to the MySQL database."""

    connection = None

    try:
        connection = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "2r546482ek83exm4",
            database = "Canbase_Reinvented"
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

# --- Example Usage ---

# Define your database credentials
DB_HOST = "localhost"  # or your server's IP address
DB_USER = "your_username"
DB_PASSWORD = "your_password"
DB_NAME = "your_database_name" # Optional: specify a database, or connect to the server first

# Call the function to connect
connection = create_db_connection(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)

# Don't forget to close the connection when you're done with your operations
if connection and connection.is_connected():
    # Perform database operations here (create cursor, execute queries, etc.)
    # ...
    connection.close()
    print("MySQL connection closed")

#Now I can import create_db_connection (a local library) to another file