import sqlite3

class DatabaseController:

    def __init__(self, dbname):
        self._connection = sqlite3.connect(dbname)
        self._cursor = self._connection.cursor()

    def select_user(self):
        pass

    def create_user(self):
        pass

    def verify_password(self, password):
        pass
