import mariadb
import dbcreds
import traceback
# This function gets a connection for the database.
def get_db_connection():
    try:
        return mariadb.connect(database=dbcreds.database, host=dbcreds.host, port=dbcreds.port, 
                               user=dbcreds.user, password=dbcreds.password)
    except:
        print("Error connecting to DB!")
        traceback.print_exc()
        return None
# This function gets a cursor for the database.      
def get_db_cursor(conn):
    try:
        return conn.cursor()
    except:
        print("Error creating cursor on DB!")
        traceback.print_exc()
        return None
# This function closes the cursor for the database.
def close_db_cursor(cursor):
    if(cursor == None):
        return True
    try:
        cursor.close()
        return True
    except:
        print("Error closing cursor on DB!")
        traceback.print_exc()
        return False
# This function closes the connection for the database.
def close_db_connection(conn):
    if(conn == None):
        return True
    try:
        conn.close()
        return True
    except:
        print("Error closing connection to DB!")
        traceback.print_exc()
        return False
