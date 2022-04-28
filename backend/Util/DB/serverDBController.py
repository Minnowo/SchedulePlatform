from ...Schedulizer.DBController.MysqlConnection import get_connection

def init_User(): 

    connection = get_connection()
    cur = connection.cursor(prepared=True)

    cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name='Users'")
    
    if cur.fetchone()[0] != 1:
        cur.execute(
            "CREATE TABLE Users (Username varchar(255),Pass varchar(255),Email varchar(255),PRIMARY KEY (Username));"
        )
        connection.commit()

    cur.close()
    connection.close()

    