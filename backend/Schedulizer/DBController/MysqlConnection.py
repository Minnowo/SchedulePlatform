import mysql.connector

from backend.secretsVPS import SQL_HOST, SQL_USERNAME, SQL_PASSWORD, SQL_DB


def get_connection():
    db_connection = None
    try:
        db_connection = mysql.connector.connect(
            host=SQL_HOST,
            user=SQL_USERNAME,
            passwd=SQL_PASSWORD,
            database=SQL_DB,
            autocommit=True  # Autocommit 1 = True, 0 = False. To check on status Server $ mysql > select @@autocommit;
        )
    except Exception as err:
        print(f"\n\tError: '{err}'")

    return db_connection
