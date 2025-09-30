import mysql.connector
from mysql.connector import Error

def create_connection(host_name, user_name, user_password, db_name):
    """
    Create and return a MySQL database connection.
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def fetch_knowledge_base(connection):
    """
    Fetch all question-answer pairs from the knowledge_base table.
    Returns a list of dictionaries with 'question' and 'answer' keys.
    """
    cursor = connection.cursor(dictionary=True)
    query = "SELECT question, answer FROM knowledge_base"
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
    finally:
        cursor.close()
