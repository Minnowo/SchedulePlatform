"""Initial connection for the MySQL database.
"""

from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()


def get_connection():
    db_connection = None
    try:
        db_connection = mysql.connector.connect(
            host=os.getenv("SQL_HOST"),  # Local host = "localhost" or "127.0.0.1"
            user=os.getenv("SQL_USERNAME"),
            passwd=os.getenv("SQL_PASSWORD"),
            database=os.getenv("SQL_DB"),
            port=os.getenv("SQL_PORT"),  # MySQL default port number is 3306.
            autocommit=True  # Autocommit 1 = True, 0 = False. To check on status Server $ mysql > select @@autocommit;
        )
    except Exception as err:
        print(f"\n\tError: '{err}'")

    return db_connection
