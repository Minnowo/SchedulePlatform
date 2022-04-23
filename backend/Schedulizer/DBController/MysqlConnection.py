"""Initial connection for the MySQL database.

TODO: Warning MySQL username, password and database are currently stored plaintext via secretsVPS.py, which is git
 ignored. Code should instead be using environment variables at the least for production.
"""

import mysql.connector

from backend.secretsVPS import SQL_HOST, SQL_USERNAME, SQL_PASSWORD, SQL_DB


def get_connection():
    db_connection = None
    try:
        db_connection = mysql.connector.connect(
            host=SQL_HOST,  # Local host = "localhost" or "127.0.0.1"
            user=SQL_USERNAME,
            passwd=SQL_PASSWORD,
            database=SQL_DB,
            port=3306,  # MySQL default port number is 3306.
            autocommit=True  # Autocommit 1 = True, 0 = False. To check on status Server $ mysql > select @@autocommit;
        )
    except Exception as err:
        print(f"\n\tError: '{err}'")

    return db_connection
