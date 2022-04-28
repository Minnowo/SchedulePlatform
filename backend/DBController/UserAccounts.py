"""UserAccounts is used to control the user accounts table on the MySQL DB.
"""

from dotenv import load_dotenv
import os

from DBController.MysqlConnection import get_connection

load_dotenv()


def __check_add_user_accounts_table():
    """Check that the user accounts table exists, if it doesn't exist make a new courses table.

    Notes:
        Table name for storing basic user account data is held in .env and not passed as a parameter.
    """
    connection = get_connection()
    cur = connection.cursor(prepared=True)
    print("got cur")

    cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name='%s'" % os.getenv("SQL_USER_TABLE"))

    if cur.fetchone()[0] != 1:
        cur.execute("CREATE TABLE %s "
                    "(username VARCHAR(30) NOT NULL, "
                    "name VARCHAR(30) NOT NULL, "
                    "password VARCHAR(255) NOT NULL, "
                    "email VARCHAR(255) NOT NULL,"
                    "PRIMARY KEY (username))"
                    % os.getenv("SQL_USER_TABLE"))
        connection.commit()

    cur.close()
    connection.close()
