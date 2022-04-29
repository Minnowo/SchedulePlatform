"""UserAccounts is used to control the user accounts table on the MySQL DB.
"""

from dotenv import load_dotenv
import os

from mysqlx import Row

#Local imports:
from Util.Authentication import auth
from DBController.MysqlConnection import get_connection

load_dotenv()

def __check_add_user_accounts_table():
    """Check that the user accounts table exists, if it doesn't exist make a new courses table.

    Notes:
        Table name for storing basic user account data is held in .env and not passed as a parameter.
    """
    connection = get_connection()
    #connection = con
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

# def get_user(username : str):

#     connection = get_connection()

#     __check_add_user_accounts_table(connection)

#     cur = connection.cursor(prepared=True)

def createUser(username: str, password: str, name: str, email: str):

    connection = get_connection()

    __check_add_user_accounts_table()
    print("Get here!")

    cur = connection.cursor(prepared=True)

    password = auth.hashPassword(password)

    # cur.execute("INSERT INTO %s (`username`,`password`, `name` , `email`) VALUES ('%s' , '%s' , '%s' , '%s')" % (os.getenv("SQL_USER_TABLE"), username, password, name, email)
    # )

    cur.execute("INSERT INTO %s VALUES ( '%s', '%s', '%s', '%s' )" % (os.getenv("SQL_USER_TABLE"), username,name, password, email))
    cur.close()
    connection.close()

def searchUser(queryString: str) -> Row:

    # queryString can either be the username or email STRING.
    if not isinstance(queryString,str):
        return None

    connection = get_connection()

    cur = connection.cursor(prepared=True)    

    cur.execute("SELECT * FROM user_accounts WHERE username = '%s' OR email = '%s'" % (queryString, queryString) )

    user = cur.fetchone()

    if isinstance(user,str):
        return user





    
