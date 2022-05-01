"""UserAccounts is used to control the user accounts table on the MySQL DB.
"""

from dotenv import load_dotenv
import os


from Util.Authentication import auth
from DBController.MysqlConnection import get_connection

from Util.Constant import InputFilter, Exceptions


load_dotenv()


def __check_add_user_accounts_table():
    """Check that the user accounts table exists, if it doesn't exist make a new courses table.

    Notes:
        Table name for storing basic user account data is held in .env and not passed as a parameter.
    """
    connection = get_connection()
    cur = connection.cursor(prepared=True)

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

def create_user(username: str, password: str, name: str, email: str):

    __check_add_user_accounts_table()   

    if InputFilter.check_username_string(username) == False:
        return Exceptions.API_406_USERNAME_INVALID

    if InputFilter.check_email_string(email) == False:
        return Exceptions.API_406_PARAM_INVALID
    
    if InputFilter.check_password_string(password) == False:
        return Exceptions.API_406_PASSWORD_INVALID

    print("Everything seems valid..")

    connection = get_connection()

    cur = connection.cursor(prepared=True)

    cur.execute("SELECT * FROM %s WHERE username = '%s' OR email = '%s'" % (os.getenv("SQL_USER_TABLE"), username, password))
    check_query = cur.fetchone()

    if check_query is None:
        pass
    elif(check_query[0] == username):
        return Exceptions.API_409_USERNAME_CONFLICT
    
    elif(check_query[3] == email):
        return Exceptions.API_409_EMAIL_CONFLICT


    #TODO Make sure that the username & email is unique / valid

    password = auth.hash_password(password)

    cur.execute("INSERT INTO %s VALUES ( '%s', '%s', '%s', '%s' )" % (
        os.getenv("SQL_USER_TABLE"), username, name, password, email))
    cur.close()
    connection.close()

def search_user(query_string: str):  
    # query_string can either be the username or email STRING.
    if not isinstance(query_string, str):
        return None

    connection = get_connection()

    cur = connection.cursor(prepared=True)

    cur.execute("SELECT * FROM user_accounts WHERE username = '%s' OR email = '%s'" % (query_string, query_string))

    return cur.fetchone()

