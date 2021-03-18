import sqlite3


class DatabaseController:
    """ Controller for database """

    def __init__(self, dbname: str):
        """ Constructor of our controller """
        self._dbname = dbname
        self._connection = None
        self._cursor = None
        self.initialization()

    def __enter__(self):
        """ method that allow us to implement with statement initialization of connection and cursor """
        try:
            self._connection = sqlite3.connect(self._dbname)
            self._cursor = self._connection.cursor()
        except Exception:
            raise RuntimeError("connection with database didn't work")

    def __exit__(self, type, value, traceback):
        """ method that allow us to implement with statement destruction of connection and cursor """
        self._cursor = self._cursor.close()
        self._connection = self._connection.close()

    def initialization(self) -> None:
        """ initialization of table needed for future purpose in database file"""
        with self:
            self._cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE,
                    password TEXT, 
                    salt TEXT,
                    algorithm TEXT
                )
                """
            )
            self._connection.commit()

    def select_user_data(self, user: str) -> tuple:
        """ selecting data of user from database

         :param user: program user """
        with self:
            self._cursor.execute(
                """
                SELECT 
                    password, salt, algorithm
                FROM 
                    users 
                WHERE 
                    name = ?
                """, [user])

            return self._cursor.fetchone()

    def create_user(self, user: str, password: str, salt: str, algorithm: str) -> None:
        """ creation of user in database

        :param user: program user
        :param password: hashed password for user
        :param salt: salt of user password
        :param algorithm: algorithm that password was hashed in"""
        with self:
            self._cursor.execute(
                """
                INSERT INTO users (name, password, salt, algorithm)
                VALUES (?, ?, ?, ?)
                """, [user, password, salt, algorithm])
            self._connection.commit()
