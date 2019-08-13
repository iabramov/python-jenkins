import sqlite3
import os.path

class DB(object):

    # static property
    conn = None

    sqlite_file = os.path.dirname(os.path.abspath(__file__))+'/users.sqlite'    # name of the sqlite database file

    def __init__(self):
        self._connect_db()

    def close(self):
        if DB.conn != None :
            self._close_db_connection()

    def _connect_db(self):
        if DB.conn != None :
            return

        # Connecting to the database file
        DB.conn = sqlite3.connect(DB.sqlite_file)
        c = DB.conn.cursor()
        # Creating a new SQLite table, sqlite does not have DATE types
        c.execute('CREATE TABLE IF NOT EXISTS user_test (username TEXT PRIMARY KEY, date_of_birth TEXT NOT NULL)')
        DB.conn.commit()
        c.execute('PRAGMA synchronous=FULL')
           
    def _close_db_connection(self):
        # Committing changes and closing the connection to the database file
        DB.conn.commit()
        DB.conn.close()